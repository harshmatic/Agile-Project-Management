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
    total_effort=ndb.ComputedProperty(lambda self:float(self.hour+(float(self.minute)/60)))
    
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
        res = self.query(ndb.AND(Time_Log.assigne_key==user,Time_Log.project_key==project,Time_Log.status==True)).order(Time_Log.assigne_key,Time_Log.project_key,Time_Log.status,Time_Log.today_date).fetch()
        return res