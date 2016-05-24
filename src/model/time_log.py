from google.appengine.ext import ndb
from model.user import *
from base import BaseClass

class Time_Log(BaseClass):
    project_key = ndb.KeyProperty(required=True)
    task_key = ndb.KeyProperty(required=True)
    assigne_key =ndb.KeyProperty(required=True)
    today_date = ndb.DateProperty()
    hour=ndb.IntegerProperty()
    minute=ndb.IntegerProperty()
    billable =ndb.BooleanProperty()
    description =ndb.StringProperty()
 #   task_completed=ndb.BooleanProperty()
    
    def set(self):
        self.put()
    def get_all(self): 
        return self.query().fetch()
    def getall(self):
        res = self.query().fetch()
        return res
    def getByTask(self,task):
        res = self.query(Time_Log.task_key==task).fetch()
        return res
    def getByProjectUser(self,project,user):
        res = self.query(ndb.AND(Time_Log.assigne_key==user,Time_Log.project_key==project)).fetch()
        return res