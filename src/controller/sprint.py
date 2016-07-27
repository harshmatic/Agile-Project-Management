from google.appengine.ext import ndb
import logging
import model
from model import user,project
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import sprint,task,effort_estimation
from datetime import datetime
from model import project
from google.appengine.api.taskqueue import taskqueue 
from model import product_backlog
from common import checkdomain
from model.sprint import Sprint_Status
from model.status import Status
from model.tag import Tags
from google.appengine.datastore.datastore_query import Cursor

class Tasks(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        #if check_permission(self):
            key=self.session['current_project']  
            type_data=task.Type().get_all()
            team=project.ProjectMembers().get_all(key)
            complexity=project.Estimation().get_all(key)
            logging.info(complexity)
            sprints = sprint.Sprint().get_by_project(key)
            tags=model.tag.Tags().get_tags(project=key)
            
            self.render_template("user_new/addtask.html",{"type":type_data,"team":team,"complex":complexity,'sprints':sprints,"tags":tags})
        #else:
            #self.response.write("you are not allowed")
    
    @checkdomain
    def post(self,*args,**kargs):
        task_data=task.Task()
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        task_data.name = self.request.get('name')
        task_data.description = self.request.get('desc')
        task_data.actual_efforts = self.request.get('actual_efforts')
        
        if (self.request.get('complexity') != 'None'):
            task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        else:
            task_data.complexity=None
            
        if (self.request.get('tag') != 'None'):
            task_data.tag = ndb.Key(urlsafe=self.request.get('tag'))
        else:
            task_data.tag=None
        
        if (self.request.get("start") != ''):
            task_data.startDate = datetime.strptime(self.request.get("start"), '%m/%d/%Y').date()
        else:
            task_data.startDate=None
        
        if (self.request.get("end")!=''):
            task_data.endDate = datetime.strptime(self.request.get("end"), '%m/%d/%Y').date()
        else:
            task_data.endDate=None    
            
        if (self.request.get('assignee') != 'None'):
            task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        else:
            task_data.assignee=None
            
        task_data.efforts=0.0
            
        if (self.request.get('sprint') != 'None'):
            sprint_key = ndb.Key(urlsafe=self.request.get('sprint'))
            task_data.sprint=sprint_key
            sprint_data=sprint_key.get()
            sprint_data.sprint_status=Sprint_Status[0]
            sprint_data.put()
            logging.info(sprint_data)
        else:
            task_data.sprint=None
            
            
            
        if (self.request.get('user_story') != 'None'):
            task_data.user_story = ndb.Key(urlsafe=self.request.get('user_story'))   
        else:
            task_data.user_story=None
        
       # task_data.project = ndb.Key(urlsafe=self.request.get('key'))
        
        task_data.project=self.session['current_project']  
        
        task_data.createdby = createdBy
        task_data.type = ndb.Key(urlsafe=self.request.get('type'))
        
        
        task_data.task_status = "Open"
        
        
        task_data.created_by = currentUser['email_address']
        task_data.status = True
        task_data.put()
        
        
        self.response.out.write("true")
        
        
class EditTask(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        #if check_permission(self):
            edit_key=ndb.Key(urlsafe=self.request.get('edit_key'))
            task_data=edit_key.get()
            key=self.session['current_project']
            type_data=task.Type().get_all()
            team=project.ProjectMembers().get_all(key)
            complexity=project.Estimation().get_all(key)
            sprints = sprint.Sprint().get_by_project(key)
            
            tags=model.tag.Tags().get_tags(project=key)
            self.render_template("user_new/edittask.html",{"type":type_data,"team":team,"complex":complexity,'sprints':sprints,'task_data':task_data,"tags":tags})
        #else:
            #self.response.write("you are not allowed")
    
    @checkdomain
    def post(self,*args,**kargs):
        logging.info(type(self.request.get('edit_key')))
        task_key = ndb.Key(urlsafe=self.request.get('edit_key'))
        task_data=task_key.get()
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        task_data.name = self.request.get('name')
        task_data.description = self.request.get('desc')
        
        if(self.request.get("start") != ''):
            try:
                task_data.startDate = datetime.strptime(self.request.get("start"), '%m/%d/%Y').date()
            except:
                d = datetime.strptime(self.request.get("start"), '%d/%m/%Y').strftime('%m/%d/%Y')
                task_data.startDate = datetime.strptime(d, '%m/%d/%Y').date()
        else:
            task_data.startDate=None
        
        
        if(self.request.get("end") != ''):
            try:
                task_data.endDate = datetime.strptime(self.request.get("end"), '%m/%d/%Y').date()
            except:
                d = datetime.strptime(self.request.get("end"), '%d/%m/%Y').strftime('%m/%d/%Y')
                task_data.endDate = datetime.strptime(d, '%m/%d/%Y').date()
        else:
            task_data.endDate=None
        
        
        if (self.request.get('complexity') != 'None'):
            task_data.complexity = ndb.Key(urlsafe=self.request.get('complexity'))
        else:
           task_data.complexity=None
        
        if (self.request.get('assignee') != 'None'):
            task_data.assignee = ndb.Key(urlsafe=self.request.get('assignee'))
        else:
           task_data.assignee=None
           
        if (self.request.get('tag') != 'None'):
            task_data.tag = ndb.Key(urlsafe=self.request.get('tag'))
        else:
            task_data.tag=None
        
        if (self.request.get('sprint') != 'None'):
            sprint_key = ndb.Key(urlsafe=self.request.get('sprint'))
            task_data.sprint=sprint_key
            sprint_data=sprint_key.get()
            sprint_data.sprint_status=Sprint_Status[0]
            sprint_data.put()
            logging.info(sprint_data)
        else:
            task_data.sprint=None
        
        if (self.request.get('user_story') != 'None'):
            task_data.user_story = ndb.Key(urlsafe=self.request.get('user_story'))  
        else:
            task_data.user_story =None
        
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
        

class MoveTask(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        key=self.session['current_project']
        task_key=ndb.Key(urlsafe= self.request.get('task_key'))
        task_info=task_key.get()
        sprints = sprint.Sprint().get_by_project(key)
        self.render_template("user_new/movetask.html",{'sprints':sprints,"task_info":task_info})
    
    @checkdomain 
    def post(self,*args,**kargs):
        sprint_name=ndb.Key(urlsafe=self.request.get('sprint_name'))
        task_key=ndb.Key(urlsafe=self.request.get('task_key'))
        task_data=task_key.get()
        task_data.sprint=sprint_name
        task_data.put()
        self.response.out.write("true")
        
        
class DeleteTask(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        #if check_permission(self):
            edit_key=ndb.Key(urlsafe=self.request.get('delete_key'))
            task_data=edit_key.get()
            self.render_template("user_new/deletetask.html",{'task_data':task_data})
        #else:
            #self.response.write("you are not allowed")
    @checkdomain
    def post(self,*args,**kargs):
        key= ndb.Key(urlsafe=self.request.get('delete_key'))
        task_key=key.get()
         
        user_info = self.auth.get_user_by_session()
        task_key.modified_by = user_info['email_address']
        task_key.modified_date = datetime.now()
        task_key.status = False
           
        task_key.put()
            #user_key.delete()  
        self.response.write("true")     

class SprintDD(BaseHandler):
    def get(self,*args,**kargs):
        if self.session['current_project']:
            logging.info("Inside")
            project1 =self.session['current_project']   
            sprint_data=sprint.Sprint().get_by_project(project1)
            self.render_template("user_new/dropdown_sprint.html", {"sprint":sprint_data})
        
        
            
class Sprint(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        if check_permission(self):
        
            project1 =self.session['current_project']   
            all_sprint=sprint.Sprint().get_sprints(project=project1)
            
            #release=project.ProjectRelease()
            #releases=release.get_by_project(project1)
            
            releases=project.ProjectRelease().get_releases(project=project1)
           
            
            
            team=project.ProjectMembers().get_all(project1)
            
            
            if not (self.request.get('sprint_key')):
                
           
                
                sprint_data=sprint.Sprint().query(sprint.Sprint.project == project1,ndb.AND(sprint.Sprint.status == True)).order(-sprint.Sprint.created_date).get()
          
                task_cursor_str=self.request.get('tp',None)
                t_cursor=None
            
                if task_cursor_str:
                    t_cursor=Cursor(urlsafe=task_cursor_str)
                
                #tasks,task_next_cursor,t_more= task.Task().query(task.Task.project == project1,ndb.AND(task.Task.status == True)).order(-task.Task.created_date).fetch_page(15, start_cursor=t_cursor)
            
                tasks,task_next_cursor,t_more= task.Task().get_tasks(project=project1,start_cursor=t_cursor)
              
                if t_more:
                
                    t_next_cursor= task_next_cursor.urlsafe()
                    
                    self.render_template("user_new/apm-sprint-items.html",{"all_sprint":all_sprint,"sprints":sprint_data,"team":team,"tasks":tasks,"release":releases,"task_next_cursor":t_next_cursor})
            
                else:
                
                    self.render_template("user_new/apm-sprint-items.html",{"all_sprint":all_sprint,"sprints":sprint_data,"team":team,"tasks":tasks,"release":releases})
            
            
            else:
               
                sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
                sprint_data=sprint_key.get()
                
                task_cursor_str=self.request.get('tp',None)
                t_cursor=None
            
                if task_cursor_str:
                    t_cursor=Cursor(urlsafe=task_cursor_str)
                
               # tasks,task_next_cursor,t_more= task.Task().query(task.Task.sprint == sprint_data.key).order(-task.Task.created_date).fetch_page(15, start_cursor=t_cursor)
               
                tasks,task_next_cursor,t_more= task.Task().get_tasks(project=project1,sprint=sprint_data.key,start_cursor=t_cursor)
              
                if t_more:
                
                    t_next_cursor= task_next_cursor.urlsafe()
                    
                    self.render_template("user_new/apm-sprint-items.html",{"all_sprint":all_sprint,"sprints":sprint_data,"team":team,"tasks":tasks,"release":releases,"task_next_cursor":t_next_cursor})
            
                else:
                
                    self.render_template("user_new/apm-sprint-items.html",{"all_sprint":all_sprint,"sprints":sprint_data,"team":team,"tasks":tasks,"release":releases})
            
          
                
            
        else:
            self.response.write("you are not allowed")
    
    @checkdomain
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        createdBy=self.user_model.get_by_id(currentUser['user_id']).key
        sprint_data=sprint.Sprint()
        sprint_data.name = self.request.get("name")
        sprint_data.description = self.request.get("desc")
        sprint_data.workinghours=self.request.get("workinghours")
        
        if self.request.get("start") != '':
            sprint_data.startDate = datetime.strptime(self.request.get("start"), '%m/%d/%Y').date()
            
        if self.request.get('end') !='':
            sprint_data.endDate = datetime.strptime(self.request.get("end"), '%m/%d/%Y').date()
            
        if (self.request.get('release') != 'None'):
            sprint_data.release_key=ndb.Key(urlsafe=self.request.get('release'))
       
     #   sprint_data.project = ndb.Key(urlsafe=self.request.get("project_key"))
        
        sprint_data.project=self.session['current_project']  
        
        sprint_data.project =self.session['current_project'] 
        sprint_data.createdby = createdBy
        sprint_data.sprint_status = Sprint_Status[0]
        
        
        sprint_data.company = self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        
        sprint_data.created_by = currentUser['email_address']
        sprint_data.status = True
        
       
        
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
    @checkdomain
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
    
    @checkdomain
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
        
        
        if self.request.get("start")!='':
            sprint_data.startDate = datetime.strptime(self.request.get("start"), '%m/%d/%Y').date()
        else:
            sprint_data.startDate =None
        
        if self.request.get("end")!='':
            sprint_data.endDate = datetime.strptime(self.request.get("end"), '%m/%d/%Y').date()
        else:
            sprint_data.endDate =None

        sprint_data.project=self.session['current_project']  
       # sprint_data.sprint_status = "Open"
      #  sprint_data.company = self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        
        new_workinghours=self.request.get("new_workinghours")
        old_workinghours=self.request.get("old_workinghours")
        
        sprint_data.workinghours=new_workinghours
        
       # sprint_data.created_by = currentUser['email_address']
        sprint_data.status = True
        
        if (self.request.get('release') != 'None'):
            sprint_data.release_key=ndb.Key(urlsafe=self.request.get('release'))
        else:
            sprint_data.release_key=None
        
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
    @checkdomain
    def get(self,*args,**kargs):
        #if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
            key = ndb.Key(urlsafe=self.request.get('delete_key'))
            sprint_info=key.get()
            self.render_template("user_new/delete_sprint.html",{"sprint_info":sprint_info})
           
        #else:
            #self.response.write("you are not allowed")
    @checkdomain
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
        
        
class SprintStatus(BaseHandler):   
    @checkdomain  
    def post(self,*args,**kargs):
        
        #logging.info(self.request.get("key"))
        key=ndb.Key(urlsafe=self.request.get("key"))
        status = self.request.get('status')
        
        if(status == 'Complete Sprint'):
            tasks_data=model.task.Task().query(ndb.AND(model.task.Task.sprint == key ,ndb.AND(model.task.Task.status == True ,ndb.AND(model.task.Task.task_status.IN (['In Progress','Open','Done','ReOpen','Deferred']))))).get()
        #tasks_data=tasks.fetch(1)
        
       # count = len(tasks_data)
            logging.info(tasks_data)
        
            if tasks_data:
              #  self.render_template("user_new/task_list.html",{"tasks_data":tasks_data})
                self.response.write('false')
                
            else:
                sprint_data=key.get()
                sprint_data.sprint_status = Sprint_Status[2]
                sprint_data.put()
                self.response.write('true')
                
        if(status == 'Open Sprint'):
            sprint_data=key.get()
            sprint_data.sprint_status = Sprint_Status[0]
            sprint_data.put()
            self.response.write('true')

class PendingTaskList(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        #key=ndb.Key(urlsafe=self.request.get("key"))   
       # tasks_data=model.task.Task().query(ndb.AND(model.task.Task.sprint == key ,ndb.AND(model.task.Task.status == True ,ndb.AND(model.task.Task.task_status.IN (['In Progress','Open','Done','ReOpen','Deferred']))))).fetch()
       # self.render_template("user_new/task_list.html",{"tasks_data":tasks_data})
        project_key=self.session['current_project']
        key=ndb.Key(urlsafe=self.request.get('key'))
        sprint_data=key.get()
        completed_task=0
        pending_task=0
        open_task=0
        close_task=0
        reopen_task=0
        deferred_task=0
        
        task_data=model.task.Task().query(ndb.AND(model.task.Task.sprint == key ,ndb.AND(model.task.Task.status == True))).fetch()
        
        logging.info(task_data)
        
        for i in task_data:
            if (i.task_status == 'Open'):
                open_task=open_task+1
            if (i.task_status == 'In Progress'):
                pending_task=pending_task+1
            if (i.task_status == 'Done'):
                completed_task=completed_task+1
            if (i.task_status == 'Close'):
                close_task=close_task+1
            if (i.task_status == 'ReOpen'):
                reopen_task=reopen_task+1
            if (i.task_status == 'Deferred'):
                deferred_task=deferred_task+1
        
        sprints = sprint.Sprint().get_by_project(project_key)
        
        self.render_template("user_new/sprintstatus.html",{'sprint_data':sprint_data,'sprints':sprints,"open_task":open_task,"pending_task":pending_task,"completed_task":completed_task,"close_task":close_task,"reopen_task":reopen_task,"deferred_task":deferred_task,"task_data":task_data})
    
    @checkdomain
    def post(self,*args,**kargs):
        key=ndb.Key(urlsafe=self.request.get('sprint_key'))
        new_sprint_key=ndb.Key(urlsafe=self.request.get('sprint_data'))
     #   logging.info(new_sprint_key)
        tasks_data=model.task.Task().query(ndb.AND(model.task.Task.sprint == key ,ndb.AND(model.task.Task.status == True ,ndb.AND(model.task.Task.task_status.IN (['In Progress','Open','Done','ReOpen','Deferred']))))).fetch()
      
        task_list=[]
        
        for i in tasks_data:
            tasks_key=i.key.get()        
            
            tasks_key.sprint = new_sprint_key        
              #  tasks_key.put()        
            task_list.append(tasks_key)        
                    
                    
         #   logging.info(task_list)        
        ndb.put_multi(task_list)           
    
        self.response.out.write('true')
  
        
class SprintInfo(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        #if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
           if self.request.get('key')!= "None":
                key = ndb.Key(urlsafe=self.request.get('key'))
                sprint_info=key.get()
               # self.render_template("user_new/delete_sprint.html",{"sprint_info":sprint_info})
                
                startDate = sprint_info.startDate
                startDate=startDate.strftime('%m/%d/%Y')
                
                endDate = sprint_info.endDate
                endDate=endDate.strftime('%m/%d/%Y')
               
                params=startDate,endDate
               
                self.response.write(params)
            
            
class SprintPieChart(BaseHandler):
    def post(self,*args,**kargs):
        if (self.request.get('openscount') !=0):
            open_count=self.request.get('openscount')
        else:
            open_count = 0
        
        if (self.request.get('inprogresscount') != 0):
            inprogress_count=self.request.get('inprogresscount')
        else:
            inprogress_count = 0
            
        if (self.request.get('completedcount') != 0):
            done_count=self.request.get('completedcount')    
        else:
            done_count = 0
        self.render_template('user_new/sprint_piechart.html', {"opencount":open_count,"inprogresscount":inprogress_count,"donecount":done_count})        
            
              
            
class GetUserStory(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        productBacklog_key=[]
        if self.request.get('key')!="None":
            key = ndb.Key(urlsafe=self.request.get('key'))
            product_info=key.get()
            
            logging.info(key)
            
            productBacklog = product_backlog.ProductUserStory()
            productBacklog = productBacklog.query(product_backlog.ProductUserStory.sprintId == key).fetch()
            
            
            
            for i in productBacklog:
                if i.status == True:
                    a = dict()
                    a['value'] = i.key.urlsafe()
                    a["name"] = str(i.backlog_name)
                    productBacklog_key.append(a)
             
        logging.info(productBacklog_key)
        
        self.render_template('user_new/dropdown_userstory.html', {"stories":productBacklog_key})

class Alltags(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        key=self.session['current_project'] 
        tags=model.tag.Tags().get_tags(project=key)
        self.render_template("user_new/alltags.html",{"tags":tags})

       
    
class TagOperations(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        key=self.session['current_project'] 
        tags=model.tag.Tags().get_tags(project=key)
        
        if not (self.request.get('edit_key')):
            self.render_template("user_new/tag.html")
        else:
            tag_key=ndb.Key(urlsafe=self.request.get('edit_key'))
            tag_info=tag_key.get()
            self.render_template("user_new/tag.html",{"tag_info":tag_info})
       
    
    @checkdomain
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        
        if not (self.request.get('edit_key')):
            tag_obj=model.tag.Tags()
            title=self.request.get('tag_name')
            desc=self.request.get('desc')
        
            tag_obj.name =title
            tag_obj.project=self.session['current_project']  
            tag_obj.description =desc
            tag_obj.created_by = currentUser['email_address']
            tag_obj.status = True
            tag_obj.set()
        
        else:
            tag_key=ndb.Key(urlsafe=self.request.get('edit_key'))
            tag_obj=tag_key.get()
            title=self.request.get('tag_name')
            desc=self.request.get('desc')
        
            tag_obj.name = title
            tag_obj.description = desc
            tag_obj.modified_by = currentUser['email_address']
            tag_obj.modified_date = datetime.now()
            tag_obj.set()
        
        self.response.out.write("true")
        
