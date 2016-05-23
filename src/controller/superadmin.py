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
from datetime import datetime
from google.appengine.api import users


class SuperAdminVerify(BaseHandler):
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key_user'))
        user=key.get()
        if not user.verified:
            user.verified=True
            password=user.name+user.empid
            
            user_info = self.auth.get_user_by_session()
            user.modified_by = user_info['email_address']
            user.modified_date = datetime.now()
            
            user.put()
            self.response.write("true"+password)
        else:
            self.response.write("User is already verified.")


class SuperDashboardHandler(webapp2.RequestHandler):
    def get(self):
        logging.info(self.request.url.split("://",1)[1].split(".",1)[0])
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin_new/apm-admin-dashboard.html')
        self.response.out.write(render(path,{}))
        
class SuperPermissionsHandler(webapp2.RequestHandler):
    def get(self):
        u=user.Groups()
        role=u.query(user.Groups.tenant_key==None).fetch()
        p=user.Permissions()
        perm=p.sa_get_all()
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin_new/apm-admin-permissions.html')
        self.response.out.write(render(path,{"perms":perm,"role":role}))
    def post(self):
        prev_role=""
        #role=""
        perm=[]
        #p= user.Groups()
        permission=self.request.get_all("permissions")
        permission.sort()
        for index, item in enumerate(permission):
            row=item.split("<!>")
            role1 = ndb.Key(urlsafe=row[0])
            perm1 = ndb.Key(urlsafe=row[1])
            
            if prev_role==row[0]:
                perm.append(perm1)
            else:
                if index !=0:
                    group=ndb.Key(urlsafe=prev_role).get()
                    group.permissions=perm
                    
                    user_info = self.auth.get_user_by_session()
                    group.modified_by = user_info['email_address']
                    group.modified_date = datetime.now()
                    
                    group.put()
                    perm=[]
                    prev_role=row[0]
                    perm.append(perm1)
                else:
                    prev_role=row[0]
                    perm.append(perm1) 
            logging.info(prev_role)
            logging.info(perm)      
            
        self.response.write("true")
class SuperAddPermission(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin_new/addpermission.html')
        self.response.out.write(render(path,{}))
       
    def post(self):
        url=self.request.get("perm_url")
        name=self.request.get("perm_name")
        permiss=user.Permissions()
        permiss.url=url
        permiss.permission=name
        if self.request.get("perm_order") != "":
            permiss.order=int(self.request.get("perm_order"))
        if self.request.get("perm_parent") != "":
            permiss.parentName=self.request.get("perm_parent")
        
        #user_info = self.auth.get_user_by_session()
        permiss.created_by = users.get_current_user().email()
        permiss.status = True
        
        permiss.set()
        self.response.write("true")

class SuperUsers(BaseHandler):
    def get(self):
        
        role=model.user.Groups()
        roles=role.query(user.Groups.role=="Admin").fetch(keys_only=True)
        u=user.OurUser()
        user1=u.query(user.OurUser.role==roles[0]).fetch()
        
        role1=user.Groups()
        roles1=role1.query(user.Groups.role=="Admin")
        self.render_template("superadmin_new/apm-admin-user-management.html",{"user1":user1,'roles':roles1})
        
        
        
class SuperEditRole(BaseHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        role = key.get()
        permiss=user.Permissions()
        list_per=permiss.sa_get_all()
        self.render_template("superadmin_new/editrole.html",{"role":role,"permission":list_per})
        
    def post(self):
        user_info = self.auth.get_user_by_session()
        key = ndb.Key(urlsafe=self.request.get('key_role'))
        role =key.get()
        role.role=self.request.get("role")
        perm=[]
        array_permissions=self.request.get_all("permissions")
        logging.info(array_permissions)
        for permission in array_permissions:
            perm.append(ndb.Key(urlsafe=permission))
        role.permissions=perm
        
        role.modified_by = user_info['email_address']
        role.modified_date = datetime.now()
        
        role.put()
        self.response.write("true")
               
class SuperEditPermission(BaseHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        permission = key.get()
        self.render_template("superadmin_new/editpermission.html",{"permission":permission})
        
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key_permission'))
        permission =key.get()
        permission.url=self.request.get("url_permission")
        permission.permission=self.request.get("name_permission")
        if self.request.get("perm_order") != "":
            permission.order=int(self.request.get("perm_order"))
        if self.request.get("perm_parent") != "":
            permission.parentName=self.request.get("perm_parent")
        user_info = self.auth.get_user_by_session()
        permission.modified_by = user_info['email_address']
        permission.modified_date = datetime.now()
        
        permission.put()
        self.response.write("true")        
class SuperAddRole(BaseHandler):
    def get(self):
        permiss=user.Permissions()
        list_per=permiss.sa_get_all()
        param = {"perm":list_per}
        path = os.path.join(os.path.dirname(__file__), '../view/superadmin_new/addrole.html')
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
        
        user_info = self.auth.get_user_by_session()
        u.created_by = user_info['email_address']
        u.status = True
        
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
        if tenant.query(model.user.Tenant.domain==tenant_domain).fetch():
            self.response.write('Domain already exists with the same name.')
            return
        else:
            tenant_key_added = tenant.put()
            logging.info(tenant_key_added)
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
        
        user_info = self.auth.get_user_by_session()
        created_by = user_info['email_address']
        status = True
        
        #unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
            email_address=email, name=name, password_raw=password,designation=designation,empid=empid,contact=contact,
            last_name=last_name,role=role,tenant_domain=tenant_domain,tenant_key=tenant_key,created_by=created_by,status=status, verified=False)
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
        message = mail.EmailMessage(sender="support@apm-eternus.appspotmail.com",
                            subject="Account Verification")
        message.to = email
        message.body = msg.format(url=verification_url)
        message.send()
        logging.info(msg.format(url=verification_url))
        self.response.write("true")
        

class SuperAdminEditUser(BaseHandler):
        def get(self):
            key = ndb.Key(urlsafe=self.request.get('edit_key'))
            user_info=key.get()
            logging.info(user_info)
            self.render_template("superadmin_new/edit_user.html",{"user_info":user_info})

            
            
        def post(self):
            
            tenant_domain = self.request.get('company_domain')
            tenant_name = self.request.get('company_name')
            tenant = model.user.Tenant()
            tenant.name = tenant_name
            tenant.domain = tenant_domain
            tenant.created_by = self.request.get('email')
            user_info = self.auth.get_user_by_session()
            tenant.modified_by = user_info['email_address']
            tenant.modified_date = datetime.now()
            tenant_key_added = tenant.put()
            
            key= ndb.Key(urlsafe=self.request.get('key'))
            user_key=key.get()
            
            user_key.user_name = self.request.get('email')
            user_key.email = self.request.get('email')
            user_key.name = self.request.get('first_name')
            user_key.last_name = self.request.get('last_name')
            user_key.designation = self.request.get('designation')
            user_key.empid=self.request.get('emp_id')
            user_key.contact=self.request.get('contact_no') 
            
            user_info = self.auth.get_user_by_session()
            user_key.modified_by = user_info['email_address']
            user_key.modified_date = datetime.now()
            
            user_key.put()
                        
            self.response.write("true")            
                        
class SuperDeleteRole(BaseHandler):
    def post(self,*args,**kargs):
        user_info = self.auth.get_user_by_session()
        key = ndb.Key(urlsafe=self.request.get('key_role'))
        user =key.get()
        user_info = self.auth.get_user_by_session()
        user.modified_by = user_info['email_address']
        user.modified_date = datetime.now()
        user.status = False
          
        user.put()
       # key.delete()
        self.response.write("true")
        #logging.info()
        #q=qry.filter(key in parent)
        #logging.info(qry)
 
class SuperAdminDeleteUser (BaseHandler):  
     def get(self):
         key = ndb.Key(urlsafe=self.request.get('delete_key'))
         user_info=key.get()
         logging.info(user_info)
         self.render_template("superadmin_new/delete_user.html",{"user_info":user_info})
         
     def post(self):
        key= ndb.Key(urlsafe=self.request.get('delete_key'))
        user=key.get()
        user_info = self.auth.get_user_by_session()
        user.modified_by = user_info['email_address']
        user.modified_date = datetime.now()
        user.status = False
          
        user.put()
      #   user_key.delete()  
        self.response.write("true")  
        
        
        
class SuperDeletePermission(BaseHandler):  
     def get(self):
         key = ndb.Key(urlsafe=self.request.get('key_permission'))
         user_info=key.get()
         logging.info(user_info)
         self.render_template("superadmin_new/delete_user.html",{"user_info":user_info})
         
     def post(self):
        key= ndb.Key(urlsafe=self.request.get('key_permission'))
        user=key.get()
        
        user.modified_by = users.get_current_user().email()
        user.modified_date = datetime.now()
        user.status = False
          
        user.put()
      #   user_key.delete()  
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