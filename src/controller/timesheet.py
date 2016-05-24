from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime

class Timesheet(BaseHandler):
    
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        logs=time_log.Time_Log().getByProjectUser(projectKey,currentUser)
        for l in logs:
            logging.info(l.today_date.weekday())
        self.render_template("user_new/timesheet.html",{"logs":logs})
