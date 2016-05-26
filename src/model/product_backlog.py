from google.appengine.ext import ndb
from base import BaseClass
from status import Status

class ProductUserStory(BaseClass):
    user_story_status = ndb.StringProperty(choices=Status)
    company_key= ndb.KeyProperty(required =  True)
    project_key= ndb.KeyProperty(required= True)
    sprintId = ndb.KeyProperty()
    type = ndb.KeyProperty()
    storyDesc = ndb.StringProperty(required= True)
    startDate = ndb.DateProperty(auto_now_add=True)
    roughEstimate = ndb.FloatProperty()
    priority = ndb.IntegerProperty()
    
    backlog_name= ndb.StringProperty()
    assignee=ndb.KeyProperty()
    
    def set(self):
        return self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    def get(self,id):
        res = ndb.Key(ProductUserStory,int(id)).get()
        return res
    def delete_entity(self,id):
        ndb.Key(ProductUserStory, int(id)).delete()
    

    
