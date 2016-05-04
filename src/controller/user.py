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


class EndUserDashboardHandler(BaseHandler):
    def get(self):
        if check_permission(self):
            
       #     current_user =self.auth.get_user_by_session()
            
         #   user = int(current_user['user_id'])
        #    user_id = repr(user).rstrip('L')
            
          #  logging.info(type(current_user['user_id']))
            
         #   user_db = OurUser.query().fetch()
            self.render_template("dashboard.html")
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
    def get(self):
       
            #current_user =self.auth.get_user_by_session()
            user_db = OurUser.query().fetch()
            user1=self.auth.get_user_by_session()
            role=self.user_model.get_by_id(user1['user_id']).role.get().role
            
         #   image_key=self.send_blob(self.OurUser.)
            
            upload_url = blobstore.create_upload_url('/profile') 
            self.render_template("profile.html",{'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
            
    def post(self):
            user_db = OurUser.query().fetch()
            
            id=self.request.get('user_id')
            upload = self.get_uploads()[0]
            
            user = self.user
            user.blob_key=upload.key()
            user.put()
            
           
             #current_user =self.auth.get_user_by_session()
            user_db = OurUser.query().fetch()
            user1=self.auth.get_user_by_session()
            role=self.user_model.get_by_id(user1['user_id']).role.get().role
            upload_url = blobstore.create_upload_url('/profile') 
           # self.render_template("profile.html",{'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
            
            self.redirect("/profile")
            