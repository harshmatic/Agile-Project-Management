from google.appengine.ext import ndb
import logging
from model import user
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
import model
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2

class AdminVerify(BaseHandler):
    def post(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key_user'))
        user=key.get()
        if not user.verified:
            user.verified=True
            password=user.name+user.empid
            user.put()
            self.response.write("true"+password)
        else:
            self.response.write("User is already verified.")
 
class Adminedit(BaseHandler):
    def post(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key_user'))
        user=key.get()
        if not user.verified:
            user.verified=True
            password=user.name+user.empid
            user.put()
            self.response.write("true"+password)
        else:
            self.response.write("User is already verified.")           
        
class AdminHome(BaseHandler):
    def get(self,*args,**kargs):
        
        if check_permission(self):
            self.render_template("admin/admin-dashboard.html")
        else:
            self.response.write("you are not allowed")
class DeleteEntity(BaseHandler):
    def post(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key_permission'))
        
        key.delete()
        self.response.write("true")
        #logging.info()
        #q=qry.filter(key in parent)
        #logging.info(qry)
class EditRole(BaseHandler):
    def get(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key'))
        role = key.get()
        permiss=user.Permissions()
        list_per=permiss.get_all()
        self.render_template("admin/editrole.html",{"role":role,"permission":list_per})
        
    def post(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key_role'))
        role =key.get()
        role.role=self.request.get("role")
        perm=[]
        array_permissions=self.request.get_all("permissions")
        logging.info(array_permissions)
        for permission in array_permissions:
            perm.append(ndb.Key(urlsafe=permission))
        role.permissions=perm
        role.put()
        self.response.write("true")

class EditPermission(BaseHandler):
    def get(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key'))
        permission = key.get()
        self.render_template("admin/editpermission.html",{"permission":permission})
        
    def post(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key_permission'))
        permission =key.get()
        permission.url=self.request.get("url_permission")
        permission.permission=self.request.get("name_permission")
        permission.put()
        self.response.write("true")
        
class AddPermissions(BaseHandler):
    def get(self,*args,**kargs):
        self.render_template("admin/addpermissions.html")
        
    def post(self,*args,**kargs):
        url=self.request.get("perm_url")
        name=self.request.get("perm_name")
        permiss=user.Permissions()
        permiss.url=url
        permiss.permission=name
        permiss.set()
        self.response.write("true")

class AddRole(BaseHandler):
    def get(self,*args,**kargs):
        permiss=user.Permissions()
        list_per=permiss.get_all()
        param = {"perm":list_per}
        self.render_template("admin/addrole.html",param)
        
    def post(self,*args,**kargs):
        url=self.request.get_all("permissions")
        logging.info(url)
        for index, item in enumerate(url):
            url[index] = ndb.Key(urlsafe=item)
        role=self.request.get("role")
        u=user.Groups()
        u.role=role
        u.tenant_domain=kargs['subdomain']
        ten=user.Tenant.query(user.Tenant.domain==kargs['subdomain']).fetch(keys_only=True)
        u.tenant_key=ten[0]
        u.permissions=url
        logging.info(url)
        u.put()
        self.response.write("true")
        
class EditPermissions(BaseHandler):
    def get(self,*args,**kargs):
        u=user.Groups()
        #user.Groups.tenant_domain==kargs['subdomain']
        role=u.query().fetch()
        logging.info(role)
        #role=u.get_all()
        p=user.Permissions()
        perm=p.get_all()
        self.render_template("admin_new/apm-admin-permissions.html",{"perm":perm,"role":role})
    def post(self,*args,**kargs):
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
                    
class AdminUserManagement(BaseHandler,blobstore_handlers.BlobstoreUploadHandler,blobstore_handlers.BlobstoreDownloadHandler):
    def get(self,*args,**kargs):
        
        role=model.user.Groups()
        roles=role.get_all()
        u=user.OurUser()
        user1=u.query(user.OurUser.tenant_domain==kargs['subdomain']).fetch()
        
        #user1 =user.OurUser().get_all()
       # logging.info(user1)
        user_json = [row.to_dict() for row in user1]
        #user_json.pop("datetime")
        logging.info(user_json)
        #user_json = json.dumps(user_json)
     #   upload_url = blobstore.create_upload_url('/admin/upload_photo')        
     #   logging.info(upload_url)
    
        self.render_template("admin/user-management.html",{"user1":user1,"user_json":user_json,"roles":roles})
        
    def post(self,*args,**kargs):
        
        currentUser=self.auth.get_user_by_session()
        submit=self.request.get('add_user')
        logging.info('submit:'+submit)
        
        
        user_name = self.request.get('email')
        email = self.request.get('email')
        name = self.request.get('first_name')
        role= ndb.Key(urlsafe=self.request.get('role'))
        logging.info(role)
        last_name = self.request.get('last_name')
        designation = self.request.get('designation')
        empid=self.request.get('emp_id')
        contact=self.request.get('contact_no')
        password = name+empid
       
        company_domain=self.user_model.get_by_id(currentUser['user_id']).tenant_domain
        company_key=self.user_model.get_by_id(currentUser['user_id']).tenant_key
        #unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
        email_address=email, name=name, password_raw=password,designation=designation,empid=empid,contact=contact,
        last_name=last_name,role=role,tenant_key=company_key,tenant_domain=company_domain, verified=False)
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
        You will be able to do so by visiting{url}"""
        message = mail.EmailMessage(sender="harshmatic@gmail.com",
                            subject="Account Verification")
        
        message.to = email
        message.body = msg.format(url=verification_url)
        message.send()
      #  self.response.write(msg.format(url=verification_url))
        logging.info(msg.format(url=verification_url))
        self.response.write("true")        
        
        
   #   else:
            

            
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self,*args,**kargs):
        
        if not blobstore.get(self.request.get('photo_key')):
            self.error(404)
        else:
            self.send_blob(self.request.get('photo_key'))


class AdminEditUser(BaseHandler):
        def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('edit_key'))
            user_info=key.get()
            logging.info(user_info)
            self.render_template("admin/edit_user.html",{"user_info":user_info})

            
            
        def post(self,*args,**kargs):
            
#             tenant_domain = self.request.get('company_domain')
#             tenant_name = self.request.get('company_name')
#             tenant = model.user.Tenant()
#             tenant.name = tenant_name
#             tenant.domain = tenant_domain
#             tenant.created_by = self.request.get('email')
#             tenant_key_added = tenant.put()
            
            key= ndb.Key(urlsafe=self.request.get('key'))
            user_key=key.get()
            
            user_key.user_name = self.request.get('email')
            user_key.email = self.request.get('email')
            user_key.name = self.request.get('first_name')
            user_key.last_name = self.request.get('last_name')
            user_key.designation = self.request.get('designation')
            user_key.empid=self.request.get('emp_id')
            user_key.contact=self.request.get('contact_no') 
            
            user_key.put()
                        
            self.response.write("true")            
                        

 
class AdminDeleteUser(BaseHandler):  
        def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('delete_key'))
            user_info = key.get()
            logging.info(user_info)
            self.render_template("admin/delete_user.html",{"user_info":user_info})
         
        def post(self,*args,**kargs):
            user_key= ndb.Key(urlsafe=self.request.get('delete_key'))
            user_key.delete()  
            self.response.write("true")                 