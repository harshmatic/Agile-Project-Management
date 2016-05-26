from google.appengine.ext import ndb
from google.appengine.api import taskqueue
import logging
from model import user,project
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import sprint,task
from datetime import datetime
from model import project

class Tasks(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            key=self.session['current_project']  
            type_data=task.Type().get_all()
            team=project.ProjectMembers().get_all(key)
            complexity=project.Estimation().get_all(key)
            logging.info(complexity)
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
        if (self.request.get('complexity') != 'None'):
            task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        task_data.startDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.endDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        if (self.request.get('assignee') != 'None'):
            task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        
       # task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        
        task_data.project=self.session['current_project']  
        
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        if (self.request.get('sprint') != 'None'):
            task_data.sprint = ndb.Key(urlsafe=self.request.get('sprint'))
        task_data.actual_efforts = self.request.get('actual_efforts')
        task_data.task_status = "Open"
        
        
        task_data.created_by = currentUser['email_address']
        task_data.status = True
        task_data.put()
        
        
        self.response.out.write("true")
class EditTask(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            edit_key=ndb.Key(urlsafe=self.request.get('edit_key'))
            task_data=edit_key.get()
            key=self.session['current_project']
            type_data=task.Type().get_all()
            team=project.ProjectMembers().get_all(key)
            complexity=project.Estimation().get_all(key)
            sprints = sprint.Sprint().get_by_project(key)
            self.render_template("user_new/edittask.html",{"type":type_data,"team":team,"complex":complexity,'sprints':sprints,'task_data':task_data})
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        task_key = ndb.Key(urlsafe=self.request.get('edit_key'))
        task_data=task_key.get()
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        task_data.name = self.request.get('name')
        task_data.description = self.request.get('desc')
        task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        task_data.startDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.endDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        
       # task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        task_data.project =self.session['current_project']   
        
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        task_data.sprint = ndb.Key(urlsafe=self.request.get('sprint'))
        task_data.actual_efforts = self.request.get('actual_efforts')
        task_data.task_status = "Open"
        task_data.modified_by = currentUser['email_address']
        task_data.modified_date = datetime.now()
        task_data.put()
        self.response.out.write("true")
            
class Sprint(BaseHandler):
    
    def get(self,*args,**kargs):
        if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
            project1 =self.session['current_project']   
            sprint_data=sprint.Sprint().get_by_project(project1)
            tasks=task.Task().get_all(project1)
            logging.info(tasks)
            
            release=project.ProjectRelease()
            releases=release.get_by_project(self.session['current_project'])
            self.render_template("user_new/apm-sprint-items.html",{"sprints":sprint_data,"tasks":tasks,"release":releases})
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
       
     #   sprint_data.project = ndb.Key(urlsafe=self.request.get("project_key"))
        
        sprint_data.project=self.session['current_project']  
        
        sprint_data.project =self.session['current_project'] 
        sprint_data.createdby = createdBy
        sprint_data.sprint_status = "Open"
        sprint_data.company = self.user_model.get_by_id(currentUser['user_id']).tenant_key
        sprint_data.workinghours=self.request.get("workinghours")
        
        sprint_data.created_by = currentUser['email_address']
        sprint_data.status = True
        

        if (self.request.get('release') != 'None'):
            sprint_data.release_key=ndb.Key(urlsafe=self.request.get('release'))
        
        sprint_data.set()

        sprintkey = sprint_data.set()
        sprintid = sprintkey.id()
        logging.info("before setting task");
        task = taskqueue.add(
            queue_name = "my-push-queue",                 
            url='/effortspersist',
            params={'sprintid': sprintid,'createdBy':createdBy})
        logging.info("after setting task")

        self.response.out.write("true")
        
        