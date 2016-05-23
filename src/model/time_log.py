from google.appengine.ext import ndb
from model.user import *
from base import BaseClass

class Time_Log(BaseClass):
    project_key = ndb.KeyProperty(required=True)
    task_key = ndb.KeyProperty(required=True)
    assigne_key =ndb.KeyProperty(required=True)
    today_date = ndb.DateProperty()
    time=ndb.FloatProperty()
    billable =ndb.BooleanProperty()
    description =ndb.StringProperty()
    task_completed=ndb.BooleanProperty()
    
    def set(self):
        self.put()
    def get_all(self): 
        return self.query().fetch()
   
   