from google.appengine.ext import ndb
import logging
from model.user import *
from base import BaseClass


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
    
    def set(self,data):
        self.put()
    def get_all(self,projectId):
        logging.info(self.query(Task.project==projectId).fetch())
        return self.query(Task.project==projectId).fetch()  
class Type(ndb.Model):
    name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    def get_all(self):
        return self.query().fetch()
    
        
    
    