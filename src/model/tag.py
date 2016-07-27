from google.appengine.ext import ndb
from model.user import *
from base import BaseClass

class Tags(BaseClass):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    project = ndb.KeyProperty()
    def set(self):
        return self.put()

    def get_tags(self,**kwargs):
        qry=self.query()   
        if 'project' in kwargs:
            qry = qry.filter(Tags.project == kwargs['project'])
        return qry.filter(Tags.status==True).order(-Tags.created_date).fetch(keys_only=True) 