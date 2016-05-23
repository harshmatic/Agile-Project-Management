from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime

class Timelog(BaseHandler):
    
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        
        timelog_key=time_log.Time_Log()
        
        timelog_key.project_key=self.session['current_project']
        
        timelog_key.task_key=ndb.Key(urlsafe=self.request.get('key'))
        
        
        timelog_key.assigne_key=self.user_model.get_by_id(currentUser['user_id']).key
        timelog_key.today_date=self.request.get('date')
        timelog_key.time=self.request.get('hours')+'.'+self.request.get('minutes')
        
        if (self.request.get('billable')):
            timelog_key.billable=True
        
        timelog_key.description=self.request.get('description')
        
        if (self.request.get('task_completed')):
            timelog_key.task_completed=True
       
        timelog_key.set()
        self.response.write('true')