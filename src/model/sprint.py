from google.appengine.ext import ndb
from model.user import *
from base import BaseClass

class Sprint(BaseClass):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    project = ndb.KeyProperty()
    company = ndb.KeyProperty()
    createdby = ndb.KeyProperty()
    sprint_status = ndb.StringProperty()
    workinghours = ndb.StringProperty()
    release_key=ndb.KeyProperty()
    def set(self):
        self.put()
    def get_all(self): 
        return self.query().fetch()
    def get_by_project(self,projId): 
        return self.query(Sprint.project == projId).fetch()
    