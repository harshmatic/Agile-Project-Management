from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime, timedelta,date
import time
from common import checkdomain


class Timesheet(BaseHandler):
    @checkdomain
    def show_timesheet(self,from_date,to_date):
        self.response.write('under construction')
    
    @checkdomain
    def get(self,*args,**kargs):
        week_number=0
        day_number=7
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        if self.request.get('from') and self.request.get('to'):
            logging.info('get')
            monday1=datetime.strptime(self.request.get('from'),'%d/%m/%Y').date()
            monday2=datetime.strptime(self.request.get('to'),'%d/%m/%Y').date()
            #monday1 = (start_date - timedelta(days=start_date.weekday()))
            #monday2 = (end_date - timedelta(days=end_date.weekday()))
            week_number=(monday2 - monday1).days/7
            day_number=(monday2 - monday1).days%7
            start=monday1
            prev_date=datetime.strftime(monday1 - timedelta(days=1),'%d/%m/%Y')
            next_date=datetime.strftime(monday2 + timedelta(days=8),'%d/%m/%Y')
        elif self.request.get('from') and not self.request.get('to'):
            dt=datetime.strptime(self.request.get('from'),'%d/%m/%Y').date()
            start = dt - timedelta(days=dt.weekday())
            week_number=0
            day_number=6
            prev_date=datetime.strftime(start - timedelta(days=1),'%d/%m/%Y')
            next_date=datetime.strftime(start + timedelta(days=8),'%d/%m/%Y')
        else:  
            dt=date.today()
            start = dt - timedelta(days=dt.weekday())
            week_number=0
            day_number=6
            prev_date=datetime.strftime(start - timedelta(days=1),'%d/%m/%Y')
            next_date=datetime.strftime(start + timedelta(days=8),'%d/%m/%Y')

        #w=(monday2 - monday1).days/7
        week=[]
        week_total=0
        for j in range(0,week_number+1):
            if j==week_number:
                d=day_number+1
            else:
                d=7
            for i in range(0,d):
                end = start + timedelta(days=i)
                
                if i == 6:
                    start=start + timedelta(days=7)
                    #range_to = end.strftime('%d/%m/%Y')
                week.append({'week_number':j+1,'date':end,'items':[],'total':0})
        
        logs=time_log.Time_Log().getByProjectUser(projectKey,currentUser)
        for w in week:
            for name in logs:
                key = name.today_date
                if key == w['date']:
                    w['items'].append(name)
                    w['total']=w['total']+name.total_effort
                    week_total=week_total+ name.total_effort
        self.render_template("user_new/timesheet.html",{"logs":week,'week_total':week_total,'previous':prev_date,'next':next_date})
    
    
        