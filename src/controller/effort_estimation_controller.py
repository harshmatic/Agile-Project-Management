from google.appengine.ext import ndb
import logging
from model import user,project,effort_estimation
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime,date,timedelta as td

class EffortEstimationView(BaseHandler):
    
    def get(self,*args,**kargs):
        
        #if check_permission(self):
            projectKey=self.session['current_project']
            sprints = sprint.Sprint().get_by_project(projectKey)
            currentUser=self.auth.get_user_by_session()
            currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            if(self.request.get("sprint_id") != ''):
             logging.info("The sprintid is"+self.request.get("sprint_id"))   
             estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(ndb.Key('Sprint',int(self.request.get("sprint_id"))))
            else:   
             estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(sprints[0].key)
            projectKey = estimates[0].project
            projectmembermodel = project.ProjectMembers()
            projmem = projectmembermodel.get_all(projectKey)
            self.render_template("user_new/apm-effort-estimation.html",{"sprint":sprints,"efforestimate":estimates,"users":projmem})
        #else:
            #self.response.write("you are not allowed")

class PersistDefaulEstimation(BaseHandler):
    
    def get(self,*args,**kargs):
        
        logging.info("The sprintid is"+self.request.get("sprinid"))
        sprintKey = ndb.Key('Sprint',int(self.request.get("sprinid")))
        sprint = sprintKey.get()
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        start_date = sprint.startDate
        end_date = sprint.endDate
        working_hours = sprint.workinghours
        projectKey = sprint.project
        
        
        projectmembermodel = project.ProjectMembers()
        projmem = projectmembermodel.get_all(projectKey)
        
        
        
        estlist= []  
        
        for mem in projmem:
            usereffort = effort_estimation.UserEffort()
            usereffort.userKey    =  mem.userid
            usereffort.userName   =  mem.userName
            usereffort.effortHours = working_hours
            estlist.append(usereffort)
            
        logging.info(estlist)  
        
        datelist= []
        d1 = start_date
        d2 = end_date

        delta = d2 - d1

        for i in range(delta.days + 1):
            estimationmodel = effort_estimation.EffortEstimation()
            estimationmodel.project = projectKey
            estimationmodel.sprint  = sprintKey
            estimationmodel.effort  = estlist  
            estimationmodel.date    =  d1 + td(days=i)
            estimationmodel.createdby = createdBy
            estimationmodel.set()
        
        logging.info(datelist)
        
class EditEffortEstimation(BaseHandler):
    
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        
        value = self.request.get("estival")
        effestKey = ndb.Key('EffortEstimation',int(self.request.get("effestid")))
        user_id = self.request.get("userid")
        
        effortmodel = effestKey.get()
        eff = effortmodel.effort
        
        for e in eff:
            logging.info(e.userKey.id())
            logging.info("the js value is"+user_id)
            if(str(e.userKey.id()) == user_id):
                logging.info("comes here user name is"+e.userName)
                e.effortHours = value
                
        
             
        effortmodel.set()
        
        self.response.write("success")
          
            