from google.appengine.ext import ndb

from model.user import *

class Project(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    team = ndb.StringProperty(repeated=True)
    
    def set(self):
        self.put()
    def get_all(self):
        res = self.query().fetch()
        return res