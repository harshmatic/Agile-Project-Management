from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
import logging
import os.path
import webapp2
import time
from model import user, effort_estimation
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
from model import sprint,task,time_log
from google.appengine.api import users
from webapp2_extras.appengine.auth.models import User
from model import project
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2
import email
from datetime import datetime
from common import checkdomain
import json
from datetime import date



class EndUserDashboardHandler(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        if check_permission(self):
            currentUser=self.auth.get_user_by_session()
            comp_key =  self.user_model.get_by_id(currentUser['user_id']).tenant_key
            currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            user=self.auth.get_user_by_session()
            #sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
            
            
            if not self.session.has_key('current_project'):
                
                projects= model.project.ProjectMembers().get_proj_by_user(comp_key,currentUser)
                if not projects:
                    
                    self.session['current_project']= None
                else:
                    self.session['current_project']=projects[0].projectid
                    
                projectKey=self.session['current_project']
                
            else:
                projectKey=self.session['current_project']
            #currentUser=self.auth.get_user_by_session()
            #currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            
            open_count=0
            inprogress_count =0
            done_count=0
            
            logging.info(projectKey)
            
            
            if(projectKey != None):
                #project_member=project.ProjectMembers().get_by_project_user(projectKey,currentUser)
                project_data=projectKey.get()
                logging.info(project_data.key)
                
                release= project.ProjectRelease().query().filter(project.ProjectRelease.projectid == project_data.key ,ndb.AND(project.ProjectRelease.created_by == user['email_address'] ,ndb.AND(project.ProjectRelease.status == True))).fetch()
                sprint_data = sprint.Sprint().query(sprint.Sprint.project == project_data.key , ndb.AND(sprint.Sprint.created_by == user['email_address'],ndb.AND(sprint.Sprint.status == True))).fetch()
                
               # release = model.project.ProjectRelease().query(model.project.ProjectRelease.projectid == project_data.key ,ndb.AND(model.project.ProjectRelease.created_by == user['email_address'] ,ndb.AND(model.project.ProjectRelease.status == True))).fetch()    
               # sprint = sprint.Sprint().query(sprint.Sprint.project == project_data.key,ndb.AND(model.sprint.Sprint.created_by == user['email_address'],ndb.AND(model.sprint.Sprint.status == True))).fetch()
            
                 
                 
                #if sprint key is present
                if (self.request.get('sprint_key')):
                    sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
                    sprint_info=sprint_key.get()
                    tasks=task.Task().query(task.Task.sprint == sprint_key).fetch()
                    logging.info(tasks)
                    for i in tasks:
                        if i.task_status == 'Open':
                            open_count=open_count+1
                        if i.task_status == 'In Progress':
                            inprogress_count=inprogress_count+1
                        if i.task_status == 'Done':
                            done_count=done_count+1  
                        
                     #changes for graph pop-up starts        
                    b = Barchart()
                    bdata = b.bdata(sprint_key)
                    v = Velocitychart()
                    vdata = v.vdata(projectKey)
                    u = Utilizationchart()
                    udata = u.udata(sprint_key)
                    
                    
                    self.render_template("user_new/apm-user-dashboard.html",{"currentUser":currentUser,"tasks":tasks,"open_count":open_count,"inprogress_count":inprogress_count,"done_count":done_count,"sprint_name":sprint_info.name,"bdata":bdata,"vdata":vdata,"udata":udata,"release":release,"sprint_data":sprint_data})
                    #changes for graph pop-up ends
                    
                   # self.render_template("user_new/apm-user-dashboard.html",{"currentUser":currentUser,"tasks":tasks,"open_count":open_count,"inprogress_count":inprogress_count,"done_count":done_count,"sprint_name":sprint_info.name,})
                
                #if sprint key is not there 
                else:
                    tasks=task.Task().get_by_project_user(projectKey,currentUser)
            
                    for i in tasks:
                        if i.task_status == 'Open':
                            open_count=open_count+1
                        if i.task_status == 'In Progress':
                            inprogress_count=inprogress_count+1
                        if i.task_status == 'Done':
                            done_count=done_count+1  
                    self.render_template("user_new/apm-user-dashboard.html",{"currentUser":currentUser,"tasks":tasks,"open_count":open_count,"inprogress_count":inprogress_count,"done_count":done_count,"release":release,"sprint_data":sprint_data})
                
            
            else:
                
                self.render_template("user_new/apm-user-dashboard.html",{"tasks":None,"open_count":0,"inprogress_count":0,"completed_count":0})
        else:
            self.response.write("you are not allowed")
            

class ResourceWorkload(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
        logging.info(sprint_key)
    
        estimates = effort_estimation.EffortEstimation().get_esti_by_sprint(sprint_key)
      #  logging.info(estimates)
        
        
        project=self.session['current_project']
        
        project_member=model.project.ProjectMembers().query(model.project.ProjectMembers.projectid == project ,ndb.AND(model.project.ProjectMembers.status == True)).fetch()
       # logging.info(project_member)
        
        sprint_info=sprint_key.get()
        
        if( sprint_info.startDate and  sprint_info.endDate):
            sprint_duration= sprint_info.endDate - sprint_info.startDate
            sprint_duration=sprint_duration.days
       # logging.info(sprint_duration)
        
        
            data = {}
            user_list=[]
            no_of_hours_per_user=[]
            total_hours=[]
            newlist=[]
        
            for i in estimates:
          #  for members in project_member:
                efforts = i.effort
                for j in efforts:
                        t=dict()
            #t['total']=i.total_effort
                        t=i.total_effort 
                        total= int(float(t)) * float(sprint_duration)
                        if total not in total_hours: 
                            total_hours.append(total)
                            
                #    if (members.userid == j.userKey):
                        u=dict()
                        user_info=j.userKey.get()
                        u['user']=user_info.name +' '+user_info.last_name
                        u['hours']=(int(j.effortHours) * sprint_duration)
                        
                        #u['hours']=j.effortHours
                        
                        
                       # complete_hours= int(hours)  * sprint_duration
                        
                      #  if hours not in no_of_hours_per_user:
                       #     no_of_hours_per_user.append(hours)
                       # logging.info(u)
                        if u not in user_list:
                            user_list.append(u)
                            
                       #     hours=j.effortHours 
                       #     no_of_hours_per_user.append(hours)
                        #    h = int(hours) * sprint_duration
                       #     a='['+u +','+ str(h) +']'
                       #     if a not in newlist:
                        #        newlist.append(a)
                            
                            
           # logging.info(i)  
                t=dict()
            #t['total']=i.total_effort
                t=i.total_effort 
                total= int(float(t)) * float(sprint_duration)
                if total not in total_hours: 
                    total_hours.append(total)
        
        
        
            total_hours_user=[]
            for hours in no_of_hours_per_user:
                total_hours_user.append(int(hours) * sprint_duration)
        
            count_user=len(user_list)
            count_total_hours=len(total_hours_user)
     
       
            data = {}
       
        
       # data=[user_list, no_of_hours_per_user,total_hours,sprint_duration.days]
        
        
            data['user'] = str(user_list).strip('[]')
       # data['no_of_hours_per_user'] = str(total_hours_user).strip('[]')
       # data['total_hours'] = str(total_hours).strip('[]')
      #  data['newlist'] = str(newlist).strip('[]')
        
          
        #self.response.write(json.dumps(data, ensure_ascii=False))
        #self.response.write(user_list)

            self.render_template('user_new/resource_piechart.html', {"user_list":user_list})
        
        else:
            self.response.write("No resource workload chart exists as sprint start date or end date is missing.")
        
#class ProjectManagementHandler(BaseHandler):
 #   def get(self):
   #     if check_permission(self):
            
     #       self.render_template("project.html",{'permission':'success'})
   #     else:
            #self.response.write("you are not allowed")
    #        self.render_template("project.html",{'permission':'you are not authorized to view this page'})
            
            
class SprintChart(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        
        sprint_key=ndb.Key(urlsafe=self.session['sprint'])
        sprint_info=sprint_key.get()
        tasks=task.Task().query(task.Task.sprint == sprint_key).fetch()
        logging.info(tasks)
        
        open_count=0
        inprogress_count =0
        done_count=0
        
        for i in tasks:
            if i.task_status == 'Open':
                open_count=open_count+1
            if i.task_status == 'In Progress':
                inprogress_count=inprogress_count+1
            if i.task_status == 'Done':
                done_count=done_count+1   
        
        self.render_template("user_new/sprint_piechart.html",{"open_count":open_count,"inprogress_count":inprogress_count,"done_count":done_count})
                
 
 
            
class EndUserProfile(BaseHandler,blobstore_handlers.BlobstoreUploadHandler,blobstore_handlers.BlobstoreDownloadHandler):
    @checkdomain
    def get(self,*args,**kargs):
       
            #current_user =self.auth.get_user_by_session()
            user_db = OurUser.query().fetch()
            user1=self.auth.get_user_by_session()
            role=self.user_model.get_by_id(user1['user_id']).role.get().role
            
            user = self.user
            
            if user.blob_key:
                 user_image= blobstore.get(user.blob_key)
            
            else :
                 user_image=""
            
            
            logging.info(user_image)
            
            
         #   image_key=self.send_blob(self.OurUser.)
            
            upload_url = blobstore.create_upload_url('/profile') 
            
        #    self.response.headers['Content-Type'] = 'image/png'
           
            
            self.render_template("user_new/profile.html",{'user_image':user.blob_key,'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
    
    @checkdomain        
    def post(self,*args,**kargs):
         user_db = OurUser.query().fetch()
          
         user = self.user
       #  logging.info(self.get_uploads()[0])
          
       #  logging.info(self.request.get('file'))  
         if (self.request.get('file')):
         #   a=len(self.get_uploads()[0])
        #    logging.info(a)
            try:
           # if (self.request.get('filename') != ''):
                upload = self.get_uploads()[0]
                user.blob_key=upload.key()
              #  logging.info("hello")
              #  logging.info(upload.key())
         
                
                user_name = self.request.get('email')
                email = self.request.get('email')
                name = self.request.get('first_name')
          #  role= ndb.Key(urlsafe=self.request.get('role'))
        #    logging.info(role)
                last_name = self.request.get('last_name')
                designation = self.request.get('designation')
                empid=self.request.get('emp_id')
                contact=self.request.get('contact_no')
            
           # id=self.request.get('user_id')
            
            
            
            
                user.name=name
                user.last_name=last_name
                user.email=email
                user.designation=designation
                user.empid=empid
                user.contact=contact
         
                user_info = self.auth.get_user_by_session()
                user.modified_by = user_info['email_address']
                user.modified_date = datetime.now()
         
                user.put()
            
           
             #current_user =self.auth.get_user_by_session()
                user_db = OurUser.query().fetch()
                user1=self.auth.get_user_by_session()
                role=self.user_model.get_by_id(user1['user_id']).role.get().role
                upload_url = blobstore.create_upload_url('/profile') 
           # self.render_template("profile.html",{'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
                self.redirect("/profile")
            
            except (IndexError, ValueError):
                
                user_name = self.request.get('email')
                email = self.request.get('email')
                name = self.request.get('first_name')
          #  role= ndb.Key(urlsafe=self.request.get('role'))
        #    logging.info(role)
                last_name = self.request.get('last_name')
                designation = self.request.get('designation')
                empid=self.request.get('emp_id')
                contact=self.request.get('contact_no')
            
           # id=self.request.get('user_id')
            
            
            
            
                user.name=name
                user.last_name=last_name
                user.email=email
                user.designation=designation
                user.empid=empid
                user.contact=contact
         
                user_info = self.auth.get_user_by_session()
                user.modified_by = user_info['email_address']
                user.modified_date = datetime.now()
         
                user.put()
            
           
             #current_user =self.auth.get_user_by_session()
                user_db = OurUser.query().fetch()
                user1=self.auth.get_user_by_session()
                role=self.user_model.get_by_id(user1['user_id']).role.get().role
                upload_url = blobstore.create_upload_url('/profile') 
           # self.render_template("profile.html",{'permission':'success', 'user_db':user_db, 'role':role,"upload_url":upload_url})
                self.redirect("/profile")
    

            
class UserViewPhotoHandler(BaseHandler,blobstore_handlers.BlobstoreDownloadHandler):
    @checkdomain
    def get(self,*args,**kargs):
        
        if not blobstore.get(self.request.get('photo_key')):
            self.error(404)
        else:
            self.send_blob(self.request.get('photo_key'))    
            
            
# class for chart pop-up starts             
            
class Barchart(BaseHandler):
    
    def bdata(self,sprint_key):
        #projectKey=self.session['current_project']
        #sprints = sprint.Sprint().get_by_project(projectKey)
        if(sprint_key != ''):
            #sprintid = self.request.get("sprint_id")
            sprint_key = sprint_key
        else:
            
            sprint_key = None
                
         
                    
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
        return json.dumps(listest)
        #self.render_template("user_new/bar_chart.html",{"sprint":sprints,"data":json.dumps(listest),"currentsprint":sprint_key})            
class Velocitychart(BaseHandler):
    
    def vdata(self,projkey):
        projectKey = projkey
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
                    
                         
        return json.dumps(datalist)      
        #self.render_template("user_new/velocitychart.html" ,{"data":json.dumps(datalist)})        
class Utilizationchart(BaseHandler):
  
    def udata(self,sprint_key):
        #projectKey=self.session['current_project']
        #sprints = sprint.Sprint().get_by_project(projectKey)
        if(sprint_key != ''):
            
            sprint_key = sprint_key
        else:
            
            sprint_key = None
            
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
        
        return json.dumps(datalist)     
        #self.render_template("user_new/utilization_chart.html",{"sprint":sprints,"data":json.dumps(datalist),"currentsprint":sprint_key})        
# class for chart pop-up ends        
