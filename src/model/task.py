from google.appengine.ext import ndb
import logging
from model.user import *
from base import BaseClass
from status import Status
from tag import Tags
from google.appengine.datastore.datastore_query import Cursor

DEFAULT=None
ITEMS = 15


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

    def get_tasks(self,prev_cursor_str=DEFAULT, next_cursor_str=DEFAULT,**kwargs):
        ALLTASKS=[]
        COUNT=0
        TASK_FIELD=''
        ORDER=''
        qry = self.query()
        if 'project' in kwargs:
            qry = qry.filter(Task.project==kwargs['project'])
        if 'sprint' in kwargs:
            qry = qry.filter(Task.sprint==kwargs['sprint'])
#         if 'start_cursor' in kwargs:
#             if order == 'desc':
#                 return qry.filter(Task.status==True).order(-Task.created_date).fetch_page(count, start_cursor=kwargs['start_cursor'],keys_only=True)
#             else:
#                 return qry.filter(Task.status==True).order(Task.created_date).fetch_page(count, start_cursor=kwargs['start_cursor'],keys_only=True)
#            
#         else:
#             if order == 'desc':
#                 return qry.filter(Task.status==True).order(-Task.created_date).fetch(keys_only=True) 
#             else:
#                 return qry.filter(Task.status==True).order(Task.created_date).fetch(keys_only=True) 
#          
         
        if 'count' in kwargs:
            ITEMS = int(kwargs['count'])
            
        else:
            ITEMS = 15
            
        if 'based_field' in kwargs:
            field = kwargs['based_field']
           
            if(field == 'userstory'):
                TASK_FIELD = Task.user_story
               
            elif(field == 'planned_startdate'):
                TASK_FIELD = Task.startDate
               
            elif(field == 'planned_enddate'):
                TASK_FIELD = Task.endDate
               
            else:
                TASK_FIELD = Task.actual_efforts
               
        else:
            TASK_FIELD = Task.created_date
            
        
        logging.info(TASK_FIELD) 
           
        if not prev_cursor_str and not next_cursor_str:
            if 'order' in kwargs:
                order=kwargs['order']
                if(order == 'asce'): 
                    objects, next_cursor, more = qry.filter(Task.status==True).order(TASK_FIELD).fetch_page(ITEMS,keys_only=True)
                else:
                    objects, next_cursor, more = qry.filter(Task.status==True).order(-TASK_FIELD).fetch_page(ITEMS,keys_only=True)
            else:
                objects, next_cursor, more = qry.filter(Task.status==True).order(TASK_FIELD).fetch_page(ITEMS,keys_only=True)
                 
            
            
            prev_cursor_str = ''
            if next_cursor:
                next_cursor_str = next_cursor.urlsafe()
            else:
                next_cursor_str = ''
            next_ = True if more else False
            prev = False
            
        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            if 'order' in kwargs:
                order=kwargs['order']
                if(order == 'asce'):
                    
                    objects, next_cursor, more = qry.filter(Task.status==True).order(TASK_FIELD).fetch_page(ITEMS, start_cursor=cursor,keys_only=True)
                else:
                    objects, next_cursor, more = qry.filter(Task.status==True).order(-TASK_FIELD).fetch_page(ITEMS, start_cursor=cursor,keys_only=True)
           
            else:
                objects, next_cursor, more = qry.filter(Task.status==True).order(TASK_FIELD).fetch_page(ITEMS, start_cursor=cursor,keys_only=True)
           
           
            prev_cursor_str = next_cursor_str
            if next_cursor:
                next_cursor_str = next_cursor.urlsafe()
            else:
                next_cursor_str = ''
           # next_cursor_str = next_cursor.urlsafe()
            prev = True
            next_ = True if more else False
            
        elif prev_cursor_str:
            cursor = Cursor(urlsafe=prev_cursor_str)
            if 'order' in kwargs:
                order=kwargs['order']
                if(order == 'asce'):
                    
                    objects, next_cursor, more = qry.filter(Task.status==True).order(TASK_FIELD).fetch_page(ITEMS, start_cursor=cursor,keys_only=True)
                else:
                    objects, next_cursor, more = qry.filter(Task.status==True).order(-TASK_FIELD).fetch_page(ITEMS, start_cursor=cursor,keys_only=True)
            else:
                objects, next_cursor, more = qry.filter(Task.status==True).order(TASK_FIELD).fetch_page(ITEMS, start_cursor=cursor,keys_only=True)
            
            
            objects.reverse()
            next_cursor_str = prev_cursor_str
            prev_cursor_str = next_cursor.urlsafe()
            prev = True if more else False
            next_ = True
            
        logging.info(objects)
          
        return {'objects': objects, 'next_cursor': next_cursor_str, 'prev_cursor': prev_cursor_str, 'prev': prev,
                'next': next_}

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
    
        
    
    