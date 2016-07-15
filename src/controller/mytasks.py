from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
import json as json
from model import sprint,task,time_log
from datetime import datetime
from model.status import Status
from common import checkdomain


class Comment(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        currentUserKey=self.user_model.get_by_id(currentUser['user_id']).key
        taskKey = ndb.Key(urlsafe=self.request.get('key'))
        tasks=taskKey.get()
        comment = task.Comments()
        comment.commnent_by=currentUserKey
        comment.comment=self.request.get('comment')
        comment.created_by = currentUser['email_address']
        comment.status =True
        tasks.comments.append(comment)
        tasks.put()
        self.response.write("true")
        
        
class MyTasks(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        project_member=project.ProjectMembers().get_by_project_user(projectKey,currentUser)
        logging.info(projectKey)
        logging.info(project_member)
        tasks=task.Task().get_by_project_user(projectKey,currentUser)
        
        team=project.ProjectMembers().get_all(projectKey)
        
        logging.info('da.das.dasd')
        logging.info(tasks)
        self.render_template("user_new/my_tasks.html",{"tasks":tasks,"team":team})

class MyTaskView(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        taskKey = ndb.Key(urlsafe=self.request.get('key'))
        task=taskKey.get()
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        time_log_data=time_log.Time_Log()
        
        time_log_data=time_log_data.getByTask(taskKey)
        status=task.task_status
        
        team=project.ProjectMembers().get_all(projectKey)
        
        self.render_template("user_new/view_task.html",{"task":task,"team":team,"time_log":time_log_data,"status":status,
                                                        "user_obj":currentUser})
    
    @checkdomain
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        
        timelog_key=time_log.Time_Log()
        
        timelog_key.project_key=self.session['current_project']
        
        timelog_key.task_key=ndb.Key(urlsafe=self.request.get('task_key'))
        
       # if self.request.get('sprint_key'):
        timelog_key.sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
        
        timelog_key.assigne_key=self.user_model.get_by_id(currentUser['user_id']).key
        
        if (self.request.get('date')):
            timelog_key.today_date= datetime.strptime(self.request.get('date'), '%d/%m/%Y').date()
        else:
            timelog_key.today_date=None
        
        
        t_hours =self.request.get('hours')
        if (t_hours):
            timelog_key.hour=int(t_hours)
            taskhours=int(t_hours)
        else:
            timelog_key.hour=00
            taskhours=00
        
        
        t_minutes=self.request.get('minutes')
        if (t_minutes):
            timelog_key.minute=int(t_minutes)
            taskminutes=int(t_minutes)
        else:
            timelog_key.minute=00
            taskminutes=00
        
        timelog_key.created_by=currentUser['email_address']
        timelog_key.status=True
        
        
        if (self.request.get('billable')):
            timelog_key.billable=True
        else:
            timelog_key.billable=False
        
        
        timelog_key.description=self.request.get('description')
        
        timelog_key.set()
        
        task_key = ndb.Key(urlsafe=self.request.get('task_key'))
        tasks=task_key.get()
        
        if (self.request.get('task_completed')):
       
            tasks.task_status=Status[2]
            tasks.modified_by = currentUser['email_address']
            tasks.modified_date = datetime.now()
           
        else:
            logging.info('not equal')
            tasks.task_status=Status[0]
            tasks.modified_by = currentUser['email_address']
            tasks.modified_date = datetime.now()
   
        timelog_data=time_log.Time_Log().query(time_log.Time_Log.task_key == timelog_key.task_key, ndb.AND(time_log.Time_Log.status == True)).fetch()
                    
        time=0.0
        for i in timelog_data:
            time += float(float(i.hour) + float(float(i.minute)/60) )
            logging.info(time) 
            
        tasks.efforts=time
             
        tasks.put()
    
        self.response.write('true')
        
class EditTimelog(BaseHandler):
        @checkdomain
        def get(self,*args,**kargs):
            
            key = ndb.Key(urlsafe=self.request.get('edit_key'))
            timelog_info=key.get()
            self.render_template("user_new/edit_timelog.html",{"timelog_info":timelog_info})

            
        @checkdomain    
        def post(self,*args,**kargs):
            key= ndb.Key(urlsafe=self.request.get('key'))
            timelog_key=key.get()
            currentUser=self.auth.get_user_by_session()
            
            if (self.request.get('date')):
                timelog_key.today_date= datetime.strptime(self.request.get('date'), '%d/%m/%Y').date()
      #  timelog_key.time=float(self.request.get('hours')+'.'+self.request.get('minutes'))
        
            #if (self.request.get('hours')):
                 #timelog_key.hour=int(self.request.get('hours'))
            
                
        
            #if (self.request.get('minutes')):
                #timelog_key.minute=int(self.request.get('minutes'))
            
            t_hours=self.request.get('hours')
            if (t_hours):
                timelog_key.hour=int(t_hours)
                taskhours=int(t_hours)
            else:
                timelog_key.hour=00
                taskhours=00
        
            t_minutes=self.request.get('minutes')
            if (t_minutes):
                timelog_key.minute=int(t_minutes)
                taskminutes=int(t_minutes)
            else:
                timelog_key.minute=00
                taskminutes=00
                
            timelog_key.modified_by = currentUser['email_address']
            timelog_key.modified_date= datetime.now() 
           
        
            if (self.request.get('billable')):
                timelog_key.billable=True
        
            timelog_key.description=self.request.get('description')
            
            timelog_key.set()
            task_key = ndb.Key(urlsafe=self.request.get('task_key'))
            tasks=task_key.get()
        
            if (self.request.get('task_completed')):
             
                tasks.task_status=Status[2]
                tasks.modified_by = currentUser['email_address']
                tasks.modified_date = datetime.now()
               
            else:
                logging.info('not equal')
                tasks.task_status=Status[0]
                tasks.modified_by = currentUser['email_address']
                tasks.modified_date = datetime.now()
             
           
            #for all time log
            timelog_data=time_log.Time_Log().query(time_log.Time_Log.task_key == timelog_key.task_key, ndb.AND(time_log.Time_Log.status == True)).fetch()
         
            
            
            time=0.0
            for i in timelog_data:
                
                time += float(float(i.hour) + float(float(i.minute)/60) )
                logging.info(time)   
            
            tasks.efforts=time
            
            tasks.put()
            self.response.write('true')

 
class DeleteTimelog(BaseHandler):  
        @checkdomain
        def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('delete_key'))
            timelog_info=key.get()
            self.render_template("user_new/delete_timelog.html",{"timelog_info":timelog_info})
        
        @checkdomain 
        def post(self,*args,**kargs):
            key= ndb.Key(urlsafe=self.request.get('delete_key'))
            timelog_key=key.get()
         
            user_info = self.auth.get_user_by_session()
            timelog_key.modified_by = user_info['email_address']
            timelog_key.modified_date = datetime.now()
            timelog_key.status = False
           
            timelog_key.put()
            
            key = ndb.Key(urlsafe=self.request.get('task_key'))
            tasks=key.get()
     
        
            timelog = time_log.Time_Log()
            timelog_data=timelog.query().fetch()
        
            count=0
            
            for i in timelog_data:
                if (i.status == True):
                    if (i.task_key == key):
                        count=count+1 
                   
        
            logging.info(count)                
              
            if (count != 0 ): 
                logging.info('time log exist')
                tasks.task_status=Status[2]
                tasks.modified_by = user_info['email_address']
                tasks.modified_date = datetime.now()
                tasks.put()
            else:
                logging.info('time log does not exist')
                tasks.task_status=Status[0]
                tasks.modified_by = user_info['email_address']
                tasks.modified_date = datetime.now()
                tasks.put()
    
            
            
           
            
            
            
            #user_key.delete()  
            self.response.write("true")     
            
class TaskStatusUpdate(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        status = int(self.request.get('status'))
        currentUser=self.auth.get_user_by_session()
        task_key = ndb.Key(urlsafe=self.request.get('task_key'))
        tasks=task_key.get()
        tasks.task_status=Status[status]
        tasks.modified_by = currentUser['email_address']
        tasks.modified_date = datetime.now()
        tasks.put()
        #self.response.write("true")    
        
        open_count=0
        inprogress_count =0
        done_count=0
        a=[]
        
        #for sprint data 
        if(self.request.get('sprint') == 'true'):
            sprint_key=tasks.sprint
            sprint_info=sprint_key.get()
            tasks=task.Task().query(task.Task.sprint == sprint_key).fetch()
            #logging.info(tasks)
        
            for i in tasks:
            
                if i.task_status == 'Open':
                    open_count=open_count+1
               
                if i.task_status == 'In Progress':
                    inprogress_count=inprogress_count+1
                
                if i.task_status == 'Done':
                    done_count=done_count+1   
                
            a=[open_count,inprogress_count,done_count]   
        
            self.response.write(a)
        else:
            projectKey=self.session['current_project']
            currentUser=self.auth.get_user_by_session()
            currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            
            tasks=task.Task().get_by_project_user(projectKey,currentUser)
                
                    
            for i in tasks:
                if i.task_status == 'Open':
                    open_count=open_count+1
                if i.task_status == 'In Progress':
                    inprogress_count=inprogress_count+1
                if i.task_status == 'Done':
                    done_count=done_count+1  
                    
            a=[open_count,inprogress_count,done_count]   
        
            self.response.write(a)
        
class AddTimelog(BaseHandler):  
        @checkdomain
        def get(self,*args,**kargs):
            taskKey = ndb.Key(urlsafe=self.request.get('key'))
            task=taskKey.get()
            status=task.task_status
            self.render_template("user_new/add_timelog.html",{"task_key":taskKey,"status":status})