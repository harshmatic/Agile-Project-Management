from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import sprint,task
from datetime import datetime

class Tasks(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            key=ndb.Key(urlsafe=self.request.get('key'))
            type_data=task.Type().get_all()
            team=project.ProjectMembers().get_all(key)
            complexity=project.Estimation().get_all(key)
            sprints = sprint.Sprint().get_by_project(key)
            self.render_template("user_new/addtask.html",{"type":type_data,"team":team,"complex":complexity,'sprints':sprints})
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        task_data=task.Task()
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        task_data.name = self.request.get('name')
        task_data.description = self.request.get('desc')
        task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        task_data.startDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.endDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        task_data.sprint = ndb.Key(urlsafe=self.request.get('sprint'))
        task_data.actual_efforts = self.request.get('actual_efforts')
        task_data.status = "Open"
        task_data.put()
        self.response.out.write("true")
class EditTask(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            edit_key=ndb.Key(urlsafe=self.request.get('edit_key'))
            task_data=edit_key.get()
            key=ndb.Key(urlsafe=self.request.get('key'))
            type_data=task.Type().get_all()
            team=project.ProjectMembers().get_all(key)
            complexity=project.Estimation().get_all(key)
            sprints = sprint.Sprint().get_by_project(key)
            self.render_template("user_new/edittask.html",{"type":type_data,"team":team,"complex":complexity,'sprints':sprints,'task_data':task_data})
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        task_data=task.Task()
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        task_data.name = self.request.get('name')
        task_data.description = self.request.get('desc')
        task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        task_data.startDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.endDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        task_data.sprint = ndb.Key(urlsafe=self.request.get('sprint'))
        task_data.actual_efforts = self.request.get('actual_efforts')
        task_data.status = "Open"
        task_data.put()
        self.response.out.write("true")
            
class Sprint(BaseHandler):
    
    def get(self,*args,**kargs):
        if check_permission(self):
            project = ndb.Key(urlsafe=self.request.get("key"))
            sprint_data=sprint.Sprint().get_by_project(project)
            tasks=task.Task().get_all(project)
            logging.info(tasks)
            self.render_template("user_new/apm-sprint-items.html",{"sprints":sprint_data,"tasks":tasks})
        else:
            self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        sprint_data=sprint.Sprint()
        sprint_data.name = self.request.get("name")
        sprint_data.description = self.request.get("desc")
        sprint_data.startDate = datetime.strptime(self.request.get("start"), '%m/%d/%Y').date()
        sprint_data.endDate = datetime.strptime(self.request.get("end"), '%m/%d/%Y').date()
        sprint_data.project = ndb.Key(urlsafe=self.request.get("project_key"))
        sprint_data.createdby = createdBy
        sprint_data.status = "Open"
        sprint_data.company = self.user_model.get_by_id(currentUser['user_id']).tenant_key
        sprint_data.workinghours=self.request.get("workinghours")
        sprint_data.set()
        self.response.out.write("true")
        
        