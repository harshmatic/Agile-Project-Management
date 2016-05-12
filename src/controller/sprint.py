from google.appengine.ext import ndb
import logging
from model import user
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import sprint

from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2

class Tasks(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            types_task=task.Type().get_all()
            self.render_template("user_new/apm-sprint-items.html",{"type":types_task})
        #else:
            #self.response.write("you are not allowed")
    
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
            
class Sprint(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            sprint_data=sprint.Sprint().get_all()
            self.render_template("user_new/apm-sprint-items.html",{"type":sprint_data})
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        sprint=sprint.Sprint()
        sprint.name = self.request.get("name")
        sprint.description = self.request.get("desc")
        sprint.startDate = self.request.get("start")
        sprint.endDate = self.request.get("end")
        sprint.project = self.request.get("project_key")
        sprint.createdby = createdBy
        sprint.status = "Open"
        sprint.set()
        self.response.out.write("true")
        
        