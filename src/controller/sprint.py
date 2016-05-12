from google.appengine.ext import ndb
import logging
from model import user
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import sprint
from datetime import datetime

class Tasks(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            types_task=sprint.Type().get_all()
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
        sprint_data=sprint.Sprint()
        sprint_data.name = self.request.get("name")
        sprint_data.description = self.request.get("desc")
        sprint_data.startDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        sprint_data.endDate = datetime.strptime(self.request.get("end"), '%d/%m/%Y').date()
        sprint_data.project = ndb.Key(urlsafe=self.request.get("project_key"))
        sprint_data.createdby = createdBy
        sprint_data.status = "Open"
        sprint_data.company = self.user_model.get_by_id(currentUser['user_id']).tenant_key
        sprint_data.set()
        self.response.out.write("true")
        
        