from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import sprint,task,effort_estimation
from datetime import datetime
from model import project
from google.appengine.api.taskqueue import taskqueue 

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
        task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        task_data.startDate = datetime.strptime(self.request.get("start"), '%d/%m/%Y').date()
        task_data.endDate = datetime.strptime(self.request.get("end"), '%d/%m/%Y').date()
        if (self.request.get('assignee') != 'None'):
            task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        if (self.request.get('sprint') != 'None'):
            task_data.sprint = ndb.Key(urlsafe=self.request.get('sprint'))
        
       # task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        
        task_data.project=self.session['current_project']  
        
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        
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
        if (self.request.get('assignee') != 'None'):
            task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        if (self.request.get('sprint') != 'None'):
            task_data.sprint = ndb.Key(urlsafe=self.request.get('sprint'))
        
       # task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        task_data.project =self.session['current_project']   
        
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        task_data.actual_efforts = self.request.get('actual_efforts')
        task_data.task_status = "Open"
        task_data.modified_by = currentUser['email_address']
        task_data.modified_date = datetime.now()
        task_data.put()
        self.response.out.write("true")
            
class Sprint(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
            project1 =self.session['current_project']   
            sprint_data=sprint.Sprint().get_by_project(project1)
            tasks=task.Task().get_all(project1)
            logging.info(tasks)
            
            release=project.ProjectRelease()
            releases=release.get_by_project(self.session['current_project'])
            self.render_template("user_new/apm-sprint-items.html",{"sprints":sprint_data,"tasks":tasks,"release":releases})
        #else:
            #self.response.write("you are not allowed")
    
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
        
        sprintkey = sprint_data.set()
        sprintid = sprintkey.id()
        logging.info("before setting task");
        task = taskqueue.add(
            queue_name = "my-push-queue",                 
            url='/effortspersist',
            params={'sprintid': sprintid,'createdBy':createdBy})
        logging.info("after setting task")
        self.response.out.write("true")
        
class EditSprint(BaseHandler):

    def get(self,*args,**kargs):
        #if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
            key = ndb.Key(urlsafe=self.request.get('edit_key'))
            sprint_info=key.get()
            release=project.ProjectRelease()
            releases=release.get_by_project(self.session['current_project'])
            self.render_template("user_new/editsprint.html",{"sprint_info":sprint_info,"release":releases})
           
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        sprint_key = ndb.Key(urlsafe=self.request.get('edit_key'))
        sprint_data=sprint_key.get()
        
        currentUser=self.auth.get_user_by_session()
       # modified_by=self.user_model.get_by_id(currentUser['user_id']).key
        sprint_data.modified_by=currentUser['email_address']
        sprint_data.modified_date = datetime.now()
       # sprint_data=sprint.Sprint()
        sprint_data.name = self.request.get("name")
        sprint_data.description = self.request.get("desc")
        sprint_data.startDate = datetime.strptime(self.request.get("start"), '%m/%d/%Y').date()
        sprint_data.endDate = datetime.strptime(self.request.get("end"), '%m/%d/%Y').date()

        sprint_data.project=self.session['current_project']  
        sprint_data.sprint_status = "Open"
      #  sprint_data.company = self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        
        new_workinghours=self.request.get("new_workinghours")
        old_workinghours=self.request.get("old_workinghours")
        
        sprint_data.workinghours=new_workinghours
        
       # sprint_data.created_by = currentUser['email_address']
        sprint_data.status = True
        
        if (self.request.get('release') != 'None'):
            sprint_data.release_key=ndb.Key(urlsafe=self.request.get('release'))
        
        sprintkey = sprint_data.set()
        sprintid = sprintkey.id()
        logging.info(sprintkey)
        if (new_workinghours != old_workinghours):
            logging.info("before setting new task");
            estimate= effort_estimation.EffortEstimation()
          #  logging.info(estimate)
            logging.info(self.session['current_project'])
            estimate_data=estimate.query(effort_estimation.EffortEstimation.sprint == sprint_key and effort_estimation.EffortEstimation.project == self.session['current_project']).fetch()
            logging.info(estimate_data)
            for i in estimate_data:
               logging.info(i)
               i.key.delete()
          
            logging.info("deleted")
            
            task = taskqueue.add(
            queue_name = "my-push-queue",                 
            url='/effortspersist',
            params={'sprintid': sprintid,'createdBy':currentUser['email_address']})
            logging.info("after setting new task")
           
        self.response.out.write("true")
        
class DeleteSprint(BaseHandler):

    def get(self,*args,**kargs):
        #if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
            key = ndb.Key(urlsafe=self.request.get('delete_key'))
            sprint_info=key.get()
            self.render_template("user_new/delete_sprint.html",{"sprint_info":sprint_info})
           
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        sprint_key = ndb.Key(urlsafe=self.request.get('delete_key'))
        sprint_data=sprint_key.get()
        
        user_info = self.auth.get_user_by_session()
        
        sprint_data.modified_by = user_info['email_address']
        sprint_data.modified_date = datetime.now()
        sprint_data.status = False
          
        sprint_data.put()
        
        sprintkey = sprint_data.set()
        sprintid = sprintkey.id()
        logging.info(sprintkey)
       
        logging.info("before setting new task");
        estimate= effort_estimation.EffortEstimation()
          #  logging.info(estimate)
        logging.info(self.session['current_project'])
        estimate_data=estimate.query(effort_estimation.EffortEstimation.sprint == sprint_key).fetch()
        logging.info(estimate_data)
        for i in estimate_data:
            logging.info(i)
            i.key.delete()
          
            logging.info("deleted")
       # key.delete()
        self.response.write("true")
        
           