from google.appengine.ext import ndb
import logging
from model.user import *
from base import BaseClass

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
    type = ndb.KeyProperty()
    task_status = ndb.StringProperty()
    actual_efforts = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comments,repeated=True)
    def set(self,data):
        self.put()
    def get_all(self,projectId):
        logging.info(self.query(Task.project==projectId).fetch())
        return self.query(Task.project==projectId).fetch()
    def get_by_project_user(self,projectId,userId):
        return self.query(ndb.AND(Task.project==projectId,Task.assignee==userId)).fetch() 


    
class Type(BaseClass):
    name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    def get_all(self):
        return self.query().fetch()
    
        
    
    