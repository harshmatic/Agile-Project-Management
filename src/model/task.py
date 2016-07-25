from google.appengine.ext import ndb
import logging
from model.user import *
from base import BaseClass
from status import Status

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
    user_story=ndb.KeyProperty()
    type = ndb.KeyProperty()
    task_status = ndb.StringProperty(choices=Status)
    efforts=ndb.FloatProperty()
    actual_efforts = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comments,repeated=True)
    
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
           
    
class Type(BaseClass):
    name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    def get_all(self):
        return self.query().fetch()
    
        
    
    