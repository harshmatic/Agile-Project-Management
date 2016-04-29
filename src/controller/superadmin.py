from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
from login import BaseHandler
import webapp2
import os.path
from model import user
import model
from google.appengine.api import mail
import logging


class SuperDashboardHandler(webapp2.RequestHandler):
    def get(self):
        logging.info(self.request.url.split("://",1)[1].split(".",1)[0])
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin/admin-dashboard.html')
        self.response.out.write(render(path,{}))
        
class SuperPermissionsHandler(webapp2.RequestHandler):
    def get(self):
        u=user.Groups()
        role=u.query(user.Groups.tenant_key==None).fetch()
        p=user.Permissions()
        perm=p.get_all()
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin/admin-permissions.html')
        self.response.out.write(render(path,{"perm":perm,"role":role}))

class AddPermissions(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin/addpermissions.html')
        self.response.out.write(render(path,{}))
        
    def post(self):
        url=self.request.get("perm_url")
        name=self.request.get("perm_name")
        permiss=user.Permissions()
        permiss.url=url
        permiss.permission=name
        permiss.set()
        self.response.write("true")
        
class AddRole(BaseHandler):
    def get(self):
        permiss=user.Permissions()
        list_per=permiss.get_all()
        param = {"perm":list_per}
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin/addpermissions.html')
        self.response.out.write(render(path,param))
        
    def post(self):
        url=self.request.get_all("permissions")
        logging.info(url)
        for index, item in enumerate(url):
            url[index] = ndb.Key(urlsafe=item)
        role=self.request.get("role")
        u=user.Groups()
        u.role=role
        u.permissions=url
        logging.info(url)
        u.put()
        self.response.write("true")
               
class SuperSignupAdminHandler(BaseHandler):
    def get(self):
        role=user.Groups()
        roles=role.query(user.Groups.role=="Admin")
        self.render_template('superadmin/registration_admin.html',{'roles':roles})
    def post(self):
        #role=model.user.Groups()
        tenant_domain = self.request.get('company_domain')
        tenant_name = self.request.get('company_name')
        tenant = model.user.Tenant()
        tenant.name = tenant_name
        tenant.domain = tenant_domain
        tenant.created_by = self.request.get('email')
        tenant_key_added = tenant.put()
        logging.info(tenant_key_added)
        if not tenant_key_added: #user_data is a tuple
            self.response.write('Domain already exists with the same name.')
            return
        role=ndb.Key(urlsafe=self.request.get('role'))
        user_name = self.request.get('email')
        email = self.request.get('email')
        name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        designation = self.request.get('designation')
        empid=self.request.get('emp_id')
        contact=self.request.get('contact_no')
        
        tenant_key = tenant_key_added
        password = name+empid
        #unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
            email_address=email, name=name, password_raw=password,designation=designation,empid=empid,contact=contact,
            last_name=last_name,role=role,tenant_domain=tenant_domain,tenant_key=tenant_key, verified=False)
        if not user_data[0]: #user_data is a tuple
            self.response.write('User already exists with the same email.')
            return

        user = user_data[1]
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)
        verification_url = self.uri_for('verification', type='v', user_id=user_id,signup_token=token, _full=True)
        msg = """Hi """+name+""",
        Thank you for registering on APM. Please follow the below url to activate your account.
        Remeber to change your password.
        You will be able to do so by visiting {url}"""
        message = mail.EmailMessage(sender="harshmatic@gmail.com",
                            subject="Account Verification")
        message.to = email
        message.body = msg.format(url=verification_url)
        message.send()
        logging.info(msg.format(url=verification_url))
        self.response.write("true")
        
        
config = {
    'webapp2_extras.auth': {
        'user_model': 'model.user.OurUser',
        'user_attributes': ['name','email_address']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'AIzaSyCLBiLQ5B1QJ2BGlQXvUqJysqFjjc_lw00'
    }
}