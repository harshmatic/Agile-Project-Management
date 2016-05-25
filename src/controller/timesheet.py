from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime, timedelta,date
import time
class Timesheet(BaseHandler):
    
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        
        # day = time.strftime("%d/%m/%Y")
        #dt = datetime.strptime(day, '%d/%m/%Y')
        dt=date.today()
        week=[];
        start = dt - timedelta(days=dt.weekday())
        for i in range(0,7):
            end = start + timedelta(days=i)
            week.append(end)
        log_time={}
        end = start + timedelta(days=6)
        logs=time_log.Time_Log().getByProjectUser(projectKey,currentUser)
        for name in logs:
            if name.today_date in week:
                key = name.today_date
                if key not in log_time:
                    log_time[key] = []
                    log_time[key].append(name)
                else:
                    log_time[key].append(name)
        for w in week:
            if w not in log_time:
                log_time[w] = []
        log_times=sorted(log_time.items())
        self.render_template("user_new/timesheet.html",{"logs":log_times})
