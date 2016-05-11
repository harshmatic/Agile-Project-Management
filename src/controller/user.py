from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
import logging
import os.path
import webapp2
import time
from model import user
import webapp2_extras.appengine.auth.models as auth_user
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import mail
from webapp2_extras import security
from login import BaseHandler,check_permission
from google.appengine.ext import ndb
from model.user import Permissions ,OurUser , Groups
import model
from google.appengine.api import users
from webapp2_extras.appengine.auth.models import User

from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2
import email


class EndUserDashboardHandler(BaseHandler):
    def get(self,*args,**kargs):
        if check_permission(self):
            
       #     current_user =self.auth.get_user_by_session()
            
         #   user = int(current_user['user_id'])
        #    user_id = repr(user).rstrip('L')
            
          #  logging.info(type(current_user['user_id']))
            
         #   user_db = OurUser.query().fetch()
            self.render_template("user_new/apm-user-dashboard.html")
        else:
            self.response.write("you are not allowed")
            
            
            
#class ProjectManagementHandler(BaseHandler):
 #   def get(self):
   #     if check_permission(self):
            
     #       self.render_template("project.html",{'permission':'success'})
   #     else:
            #self.response.write("you are not allowed")
    #        self.render_template("project.html",{'permission':'you are not authorized to view this page'})
            
            
            
class EndUserProfile(BaseHandler,blobstore_handlers.BlobstoreUploadHandler,blobstore_handlers.BlobstoreDownloadHandler):
    def get(self,*args,**kargs):
       
            #current_user =self.auth.get_user_by_session()
            user_db = OurUser.query().fetch()
            user1=self.auth.get_user_by_session()
            role=self.user_model.get_by_id(user1['user_id']).role.get().role
            
            user = self.user
            
            if user.blob_key:
                 user_image= blobstore.get(user.blob_key)
            
            else :
                 user_image=""
            
            
            logging.info(user_image)
            
            
         #   image_key=self.send_blob(self.OurUser.)
            
            upload_url = blobstore.create_upload_url('/profile') 
            
        #    self.response.headers['Content-Type'] = 'image/png'
           
            
            self.render_template("user_new/profile.html",{'user_image':user.blob_key,'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
            
    def post(self,*args,**kargs):
         user_db = OurUser.query().fetch()
          
         user = self.user
          
       #  logging.info(self.request.get('file'))  
         if (self.request.get('file') != ""):
                
            upload = self.get_uploads()[0]
            user.blob_key=upload.key()
            logging.info("hello")
            logging.info(upload.key())
         
                
         user_name = self.request.get('email')
         email = self.request.get('email')
         name = self.request.get('first_name')
          #  role= ndb.Key(urlsafe=self.request.get('role'))
        #    logging.info(role)
         last_name = self.request.get('last_name')
         designation = self.request.get('designation')
         empid=self.request.get('emp_id')
         contact=self.request.get('contact_no')
            
           # id=self.request.get('user_id')
            
            
            
            
         user.name=name
         user.last_name=last_name
         user.email=email
         user.designation=designation
         user.empid=empid
         user.contact=contact
         user.put()
            
           
             #current_user =self.auth.get_user_by_session()
         user_db = OurUser.query().fetch()
         user1=self.auth.get_user_by_session()
         role=self.user_model.get_by_id(user1['user_id']).role.get().role
         upload_url = blobstore.create_upload_url('/profile') 
           # self.render_template("profile.html",{'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
         self.redirect("/profile")
    

            
class UserViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self,*args,**kargs):
        
        if not blobstore.get(self.request.get('photo_key')):
            self.error(404)
        else:
            self.send_blob(self.request.get('photo_key'))    