from google.appengine.ext import ndb

from model.user import *

class Project(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    team = ndb.StringProperty(repeated=True)
    companyid = ndb.KeyProperty(repeat=True)
    
    def set(self):
        return self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    
class Estimation(ndb.Model):
    projectid =  ndb.KeyProperty(required=True)
    estimationLevel = ndb.StringProperty(required=True)
    estimationPoint = ndb.IntegerProperty(required=True)
    estimationHours = ndb.FloatProperty(required=True)
    
    def set(self):
        self.put()
    def get_all(self):
        res = self.query().fetch()
        return res