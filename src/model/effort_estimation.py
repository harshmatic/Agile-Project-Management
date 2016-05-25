from google.appengine.ext import ndb
import logging
from model.user import *
from base import BaseClass


class UserEffort(ndb.Model):
    userKey = ndb.KeyProperty()
    userName = ndb.StringProperty()
    effortHours = ndb.StringProperty()

class EffortEstimation(BaseClass):
    project = ndb.KeyProperty(required=True)
    sprint = ndb.KeyProperty(required=True)
    effort = ndb.StructuredProperty(UserEffort, repeated=True)
    date =  ndb.DateProperty(required=True)
    total_effort = ndb.StringProperty()
    
    def set(self):
        return self.put()
    
    def get_all(self):
        res = self.query().fetch()
        return res
    
    def get_esti_by_sprint(self,sprint_id):
        res = self.query(EffortEstimation.sprint==sprint_id).order(EffortEstimation.date).fetch()
        return res