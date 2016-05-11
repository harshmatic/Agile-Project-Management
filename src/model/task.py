from google.appengine.ext import ndb

from model.user import *

class Task(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    complexity = ndb.KeyProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    assignee = ndb.KeyProperty(repeated=True)
    project = ndb.KeyProperty()
    createdby = ndb.KeyProperty()
    type = ndb.StringProperty()
    status = ndb.StringProperty()
    def set(self,data):
        self.put()
    def get_all(self):
        return self.query.get_all()  
class Type(ndb.Model):
    name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    def get_all(self):
        return self.query().fetch()
    
        
    
    