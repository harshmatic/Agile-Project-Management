from google.appengine.ext import ndb

class ProductUserStory(ndb.Model):
    company_key= ndb.KeyProperty(required =  True)
    project_key= ndb.KeyProperty(required= True)
    sprintId = ndb.KeyProperty()
    type = ndb.KeyProperty()
    storyDesc = ndb.StringProperty(required= True)
    startDate = ndb.DateProperty(auto_now_add=True)
    roughEstimate = ndb.FloatProperty()
    priority = ndb.IntegerProperty()
    status = ndb.StringProperty()
    backlog_name= ndb.StringProperty()
    
    
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
    

    
