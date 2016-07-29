from google.appengine.ext import ndb
import logging
from model.user import *
from base import BaseClass
from status import Status
from tag import Tags

class Comments(BaseClass):
    comment=ndb.StringProperty()
    comment_by=ndb.KeyProperty()
    
class Task(BaseClass):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    complexity = ndb.KeyProperty()
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    assignee = ndb.KeyProperty()
    project = ndb.KeyProperty()
    sprint = ndb.KeyProperty()
    tag = ndb.KeyProperty(Tags , default=None)
    user_story=ndb.KeyProperty()
    type = ndb.KeyProperty()
    task_status = ndb.StringProperty(choices=Status)
    efforts=ndb.FloatProperty()
    actual_efforts = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comments,repeated=True)
    
    previous_efforts=None
    previous_userstory=None
    
    def set(self,data):
        self.put()
    def get_all(self,projectId):
        logging.info(self.query(Task.project==projectId).fetch())
        return self.query(Task.project==projectId).fetch()
    def get_by_project_user(self,projectId,userId):
        return self.query(ndb.AND(Task.project==projectId,Task.assignee==userId)).fetch() 

    def get_tasks(self,count=15,order="desc",**kwargs):
        qry = self.query()
        if 'project' in kwargs:
            qry = qry.filter(Task.project==kwargs['project'])
        if 'sprint' in kwargs:
            qry = qry.filter(Task.sprint==kwargs['sprint'])
        if 'start_cursor' in kwargs:
            if order == 'desc':
                return qry.filter(Task.status==True).order(-Task.created_date).fetch_page(count, start_cursor=kwargs['start_cursor'],keys_only=True)
            else:
                return qry.filter(Task.status==True).order(Task.created_date).fetch_page(count, start_cursor=kwargs['start_cursor'],keys_only=True)
           
        else:
            if order == 'desc':
                return qry.filter(Task.status==True).order(-Task.created_date).fetch(keys_only=True) 
            else:
                return qry.filter(Task.status==True).order(Task.created_date).fetch(keys_only=True) 
           
           
    def _post_put_hook(self,Future):
        current_efforts=self.actual_efforts
        previous_efforts=self.previous_efforts
        
        previous_userstory=self.previous_userstory
        current_userstory=self.user_story
        
       # logging.info(previous_userstory)
      #  logging.info(current_userstory)
        
        if self.user_story != None:
            userstory_key = self.user_story
            userstory_data = userstory_key.get()
            
           
            if(current_userstory == previous_userstory):
                a = userstory_data.actual_effort
                if (previous_efforts != current_efforts):
                
                    logging.info(userstory_data.actual_effort)
                    logging.info(a + (float(current_efforts) - float(previous_efforts)))
                
                    if (previous_efforts > current_efforts):
                        userstory_data.actual_effort= a + ( float(previous_efforts) - float(current_efforts) ) 
                    else:
                        userstory_data.actual_effort= a + (float(current_efforts) - float(previous_efforts))
               
                elif (previous_efforts == current_efforts):
                    userstory_data.actual_effort= userstory_data.actual_effort + 0.0
        
                userstory_data.put()
              
            else:
                previous_userstory_data= previous_userstory.get()
                b=previous_userstory_data.actual_effort
                
                #remove efforts from previous user story
                previous_userstory_data.actual_effort = b - float(previous_efforts)
                previous_userstory_data.put()
                
                #put new efforts in new user story
                a = userstory_data.actual_effort
                userstory_data.actual_effort= a +  float(current_efforts) 
                userstory_data.put()
                
                
                
            
         #   logging.info(userstory_data)
           
    
class Type(BaseClass):
    name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    def get_all(self):
        return self.query().fetch()
    
        
    
    