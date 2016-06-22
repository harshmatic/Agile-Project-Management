from google.appengine.ext import ndb
import logging
from model import user,project,effort_estimation
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime,date,timedelta as td
from common import checkdomain

class EffortEstimationView(BaseHandler):
    @checkdomain
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
             if not sprints:
                 estimates = None
             else:
                estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(sprints[0].key)
           # projectKey = estimates[0].project
            projectmembermodel = project.ProjectMembers()
            projmem = projectmembermodel.get_all(projectKey)
            self.render_template("user_new/apm-effort-estimation.html",{"sprint":sprints,"efforestimate":estimates,"users":projmem})
        #else:
            #self.response.write("you are not allowed")

class PersistDefaulEstimation(BaseHandler):
    
    def post(self):
        
        logging.info("The sprintid is"+self.request.get("sprintid"))
        sprintKey = ndb.Key('Sprint',int(self.request.get("sprintid")))
        sprint = sprintKey.get()
        createdBy= self.request.get("createdBy")
        start_date = sprint.startDate
        end_date = sprint.endDate
        working_hours = sprint.workinghours
        logging.info("the working hours"+working_hours)
        projectKey = sprint.project
        
        
        projectmembermodel = project.ProjectMembers()
        projmem = projectmembermodel.get_all(projectKey)
        
        total = 0
        
        estlist= []  
        
        for mem in projmem:
            usereffort = effort_estimation.UserEffort()
            usereffort.userKey    =  mem.userid
            usereffort.userName   =  mem.userName
            usereffort.effortHours = working_hours
            total =  total + float(working_hours)
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
            estimationmodel.total_effort = str(total)
            estimationmodel.set()
        
        logging.info(datelist)
        
class NewUserPersistDefaulEstimation(BaseHandler):
    
    def post(self):
        
        logging.info("The projectid is"+self.request.get("projectid"))
        logging.info("The userid is"+self.request.get("userid"))
        projectKey = ndb.Key('Project',int(self.request.get("projectid")))
        userKey = ndb.Key('OurUser',int(self.request.get("userid")))
        sprints = sprint.Sprint().get_by_project(projectKey)
        
        for spr in sprints :
            estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(spr.key)
            for est in estimates:
                total_effort = float(est.total_effort) + float(spr.workinghours)
                estlist = est.effort
                usereffort = effort_estimation.UserEffort()
                usereffort.userKey    =  userKey
                usereffort.userName   =  userKey.get().name
                usereffort.effortHours = spr.workinghours
                estlist.append(usereffort)
                est.effort = estlist
                est.total_effort = str(total_effort)
                est.set()

class DeleteUserPersistDefaulEstimation(BaseHandler):
    
    def post(self):
        
        logging.info("The projectid is"+self.request.get("projectid"))
        logging.info("The userid is"+self.request.get("userid"))
        projectKey = ndb.Key('Project',int(self.request.get("projectid")))
        userKey = ndb.Key('OurUser',int(self.request.get("userid")))
        sprints = sprint.Sprint().get_by_project(projectKey)
        
        for spr in sprints :
            estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(spr.key)
            for est in estimates:
                total_effort = est.total_effort
                if(est.date > date.today()):
                    estlist = est.effort
                    for e in estlist :
                        if(e.userKey == userKey):
                            oldval = e.effortHours
                            e.effortHours = "0"
            newtotal_effort = float(total_effort) - float(oldval)
            est.total_effort = str(newtotal_effort)
            est.set()
            
                
            
        
class EditEffortEstimation(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        
        if(self.request.get("estiper") != ''):
            logging.info("comes inside if loop")
            percentage = self.request.get("estiper")
            user_id = self.request.get("userid")
            sprint_id = self.request.get("sprintid")
            sprint_key = ndb.Key('Sprint',int(sprint_id))
            sprint = sprint_key.get()
            work_hour = sprint.workinghours
            newval = ((int(work_hour)) * (int(percentage))) / 100.0
            logging.info("the new val is"+str(newval))
            logging.info("The estiper is"+percentage+"the user_id is"+user_id+"the sprint id is"+sprint_id)
            estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(sprint_key)
            for est in estimates:
                total_effort = est.total_effort
                for eff in est.effort:
                    if(str(eff.userKey.id()) == user_id):
                        oldval = eff.effortHours
                        eff.effortHours = str(newval)
                newtotal_effort = float(total_effort) - float(oldval) + newval
                est.total_effort = str(newtotal_effort)
                est.set()
            self.response.write("reload")    
                
                
            
        else:    
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
                    oldval = e.effortHours
                    e.effortHours = value
                    
            newval = float(effortmodel.total_effort) - float(oldval) + float(value)
            effortmodel.total_effort = str(newval)     
            effortmodel.set()
            
            self.response.write("success")
            
class Barchart(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        sprints = sprint.Sprint().get_by_project(projectKey)
        if(self.request.get("sprint_id") != ''):
            sprintid = self.request.get("sprint_id")
            sprint_key = ndb.Key('Sprint',int(sprintid))
        else:
            if not sprints:
                logging.info("No Sprints created")
                sprint_key = None
                
            else:
                sprint_key = sprints[0].key
                
         
                    
        timelog = {}
        timelogmodel =  time_log.Time_Log.query(time_log.Time_Log.sprint_key==sprint_key).fetch()
        for t in timelogmodel:
            timelog[t.today_date] = float(timelog.get(t.today_date,0)) + float(t.total_effort)
        logging.info(timelog)
        listest = []
        estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(sprint_key)
        est_total = 0
        
        for est in estimates:
            est_total = float(est_total) + float(est.total_effort)
        #for t in taskmodel:
            #timelogmodel = time_log.Time_Log.query(time_log.Time_Log().task_key==t.key).fetch()
                         
        for e in estimates:
            #for time in timelogmodel:
                #total_timesheethours = 0
                #if(e.date == time.today_date):
                    #total_timesheethours = float(total_timesheethours) + float(time.total_effort)
            if e.date in timelog:        
                entry = []
                d = (e.date).strftime("%Y,%m,%d")
                entry.append(d)
                entry.append(float(est_total) - float(e.total_effort))
                entry.append(float(est_total) - float(timelog.get(e.date)))
                est_total = float(est_total) - float(e.total_effort)
                listest.append(entry)
                logging.info("the list is"+listest.__str__())
            else:
                entry = []
                d = (e.date).strftime("%Y,%m,%d")
                entry.append(d)
                entry.append(float(est_total) - float(e.total_effort))
                entry.append(None)
                est_total = float(est_total) - float(e.total_effort)
                listest.append(entry)
                logging.info("the list is"+listest.__str__())
        self.render_template("user_new/bar_chart.html",{"sprint":sprints,"data":json.dumps(listest),"currentsprint":sprint_key})
        #else:
            #self.response.write("you are not allowed")
 
class Utilizationchart(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        sprints = sprint.Sprint().get_by_project(projectKey)
        if(self.request.get("sprint_id") != ''):
            sprintid = self.request.get("sprint_id")
            sprint_key = ndb.Key('Sprint',int(sprintid))
        else:
            if not sprints:
                sprint_key = None
            else:
                sprint_key = sprints[0].key
        userest = {}
        username = {}
        userlog = {}    
        datalist = []
        entry = []
        entry.append("Name")
        entry.append("Percentage")
        datalist.append(entry);
        estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(sprint_key)
        timelogmodel =  time_log.Time_Log.query(time_log.Time_Log.sprint_key==sprint_key).fetch()
        
        for est in estimates:
            for user in est.effort:
                userest[user.userKey] = float(userest.get(user.userKey,0)) + float(user.effortHours)
                username[user.userKey] =  user.userName
        for time in timelogmodel:
            userlog[time.assigne_key] = float(userlog.get(time.assigne_key,0)) + float(time.total_effort)
        logging.info("the estimated effort is"+userest.__str__())  
        logging.info("the estimated effort is"+userlog.__str__())
        for k in userest:
            entry = []
            if(userlog.get(k) != None):
                percentage = (float(userlog.get(k)) / float(userest.get(k))) * 100 
                entry.append(username.get(k))
                entry.append(percentage)
                datalist.append(entry)
            else:
                entry.append(username.get(k))
                entry.append(0.0)
                datalist.append(entry)
            
        logging.info("the list is"+datalist.__str__())    
        self.render_template("user_new/utilization_chart.html",{"sprint":sprints,"data":json.dumps(datalist),"currentsprint":sprint_key})
        
class Velocitychart(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        taskmodel = task.Task.query(task.Task.project==projectKey).fetch()
        estmodel = project.Estimation.query(project.Estimation.projectid==projectKey).fetch()
        sprintmodel =  sprint.Sprint.query(sprint.Sprint.project==projectKey).fetch()
        
        estguidelines = {}
        commitedpoints = {}
        completedpoints = {}
        sprintentry = {}
        datalist = []
        entry = []
        entry.append("Sprint Name")
        entry.append("Commited")
        entry.append("Completed")
        datalist.append(entry)
        
        for spr in sprintmodel:
            sprintentry[spr.key] = spr.name
        
        for est in estmodel:
            estguidelines[est.key] = est.estimationPoint
            
        for tas in taskmodel :
            complexity = estguidelines.get(tas.complexity)
            commitedpoints[tas.sprint] = commitedpoints.get(tas.sprint,0) + complexity
            
            if(tas.task_status == "Done"):
                completedpoints[tas.sprint] = completedpoints.get(tas.sprint,0) + complexity
            
        
        for k in sprintentry:
            entry = []
            if(commitedpoints.get(k) != None):
                if(completedpoints.get(k) != None):
                    entry.append(sprintentry.get(k))
                    entry.append(commitedpoints.get(k))
                    entry.append(completedpoints.get(k))
                    datalist.append(entry)
                else:
                    entry.append(sprintentry.get(k))
                    entry.append(commitedpoints.get(k))
                    entry.append(0)
                    datalist.append(entry)
            else:
                    entry.append(sprintentry.get(k))
                    entry.append(0)
                    entry.append(0)
                    datalist.append(entry)
                    
                         
              
        self.render_template("user_new/velocitychart.html" ,{"data":json.dumps(datalist)})    