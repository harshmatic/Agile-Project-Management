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
        if not self.request.get('from'):
            self.response.write('asdasdh')
            return
        if not self.request.get('to'):
            self.response.write('asdasdh')
            return
        dt=date.today()
        week=[]
        week_total=0
        start = dt - timedelta(days=dt.weekday())
        for i in range(0,7):
            end = start + timedelta(days=i)
            week.append({'date':end,'items':[],'total':0})
        print week
        logs=time_log.Time_Log().getByProjectUser(projectKey,currentUser)
        for w in week:
            for name in logs:
                key = name.today_date
                if key == w['date']:
                    w['items'].append(name)
                    w['total']=w['total']+name.total_effort
                    week_total=week_total+ name.total_effort
        self.render_template("user_new/timesheet.html",{"logs":week,'week_total':week_total})
