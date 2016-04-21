from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
import logging
import os.path
import webapp2
import time
import model
import webapp2_extras.appengine.auth.models
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import mail
from webapp2_extras import security

def check_permission(self,*a,**we):
    auth = self.auth
    if not auth.get_user_by_session():
        self.redirect(self.uri_for('login'), abort=True)
    else:
        return True
class User(webapp2_extras.appengine.auth.models.User):
    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
    
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        logging.info(user_key)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp
    
        return None, None

def user_required(handler):
    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
            config['webapp2_extras.auth']['user_attributes'].
        :returns
            A dictionary with most user information
        """
        return self.auth.get_user_by_session()
    @webapp2.cached_property
    def user(self):
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None
    @webapp2.cached_property
    def user_model(self):
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
            """Shortcut to access the current session."""
            return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), '../view', view_filename)
        self.response.out.write(template.render(path, params))

    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
            'message': message
        }
        self.render_template('message.html', params)

    # this is needed for webapp2 sessions to work
    def dispatch(self):
            # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

class Main(BaseHandler):
    def get(self):
        self.render_template('main.html')
class SignupHandler(BaseHandler):
    def get(self):
        role=model.user.Groups()
        roles=role.get_all()
        logging.info(roles)
        self.render_template('auth/registration.html',{'roles':roles})
    
    def post(self):
        user_name = self.request.get('email')
        email = self.request.get('email')
        name = self.request.get('first_name')
        role= ndb.Key(urlsafe=self.request.get('role'))
        last_name = self.request.get('last_name')
        designation = self.request.get('designation')
        empid=self.request.get('emp_id')
        contact=self.request.get('contact_no')
        password = name+empid
        #unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
            email_address=email, name=name, password_raw=password,designation=designation,empid=empid,contact=contact,
            last_name=last_name,role=role, verified=False)
        if not user_data[0]: #user_data is a tuple
            self.response.write('User already exists with the same name')
            return

        user = user_data[1]
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)
        verification_url = self.uri_for('verification', type='v', user_id=user_id,signup_token=token, _full=True)
        msg = """Hi """+name+""",
        Thank you for registering on APM. Please follow the below url to activate your account.
        Remeber to change your password.
        You will be able to do so by visiting <a href="{url}">{url}</a>'"""
        message = mail.EmailMessage(sender="harshmatic@gmail.com",
                            subject="Account Verification")
        message.to = email
        message.body = msg.format(url=verification_url)
        message.send()
        self.response.write(msg.format(url=verification_url))
        
class ForgotPasswordHandler(BaseHandler):
    def get(self):
        self._serve_page()

    def post(self):
        username = self.request.get('username')

        user = self.user_model.get_by_auth_id(username)
        if not user:
            logging.info('Could not find any user entry for username %s', username)
            self._serve_page(not_found=True)
            return
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='p', user_id=user_id,
            signup_token=token, _full=True)

        msg = """Hi """+username+""",
        Thank you for registering on APM. Please follow the below url to activate your account.
        Remeber to change your password.
        You will be able to do so by visiting<a href="{url}">{url}</a>'"""
        
        message = mail.EmailMessage(sender="harshmatic@gmail.com",
                            subject="Reset Password")
        message.to = username
        message.body = msg.format(url=verification_url)
        message.send()
        self.response.write("true")
        
    def _serve_page(self, not_found=False):
        username = self.request.get('username')
        params = {
            'username': username,
            'not_found': not_found
        }
        self.render_template('auth/forgot-password.html', params)

class VerificationHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = None
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']

        # it should be something more concise like
        # self.auth.get_user_by_token(user_id, signup_token)
        # unfortunately the auth interface does not (yet) allow to manipulate
        # signup tokens concisely
        user, ts = User.get_by_auth_token(int(user_id), signup_token,"signup")
        if not user:
            logging.info('Could not find any user with id "%s" signup token "%s"',
                user_id, signup_token)
            self.abort(404)
        
        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        if verification_type == 'v':
            # remove signup token, we don't want users to come back with an old link
            self.user_model.delete_signup_token(user.get_id(), signup_token)

            if not user.verified:
                user.verified = True
                user.put()
            self.display_message('User email address has been verified.')
            return
        elif verification_type == 'p':
            # supply user to the page
            params = {
                'user': user,
                'token': signup_token
            }
            self.render_template('auth/change-password.html', params)
        else:
            logging.info('verification type not supported')
            self.abort(404)
            
class SetPasswordHandler(BaseHandler):

    @user_required
    def post(self):
        password = self.request.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.get('confirm_password'):
            self.response.write('nomatch')
            return

        user = self.user
        user.set_password(password)
        user.put()

        # remove signup token, we don't want users to come back with an old link
        self.user_model.delete_signup_token(user.get_id(), old_token)
        
        self.response.write('true')
        
class LoginHandler(BaseHandler):
    def get(self):
        self._serve_page()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        try:
            u = self.auth.get_user_by_password(username, password, remember=True,save_session=True)
            self.redirect(self.uri_for('home'))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', username, type(e))
            self._serve_page(True)

    def _serve_page(self, failed=False):
        username = self.request.get('username')
        params = {
            'username': username,
            'failed': failed
        }
        self.render_template('auth/login.html', params)
        
class LogoutHandler(BaseHandler):
    def get(self):
        self.auth.unset_session()
        self.redirect(self.uri_for('home'))

class AuthenticatedHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('auth/main.html')
        
config = {
    'webapp2_extras.auth': {
        #'user_model': 'User',
        'user_attributes': ['name','auth_ids']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'AIzaSyCLBiLQ5B1QJ2BGlQXvUqJysqFjjc_lw00'
    }
}