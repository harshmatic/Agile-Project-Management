from google.appengine.ext import ndb

class ProductBacklog(ndb.Model):
    sprintId = ndb.StringProperty()
    storyDesc = ndb.StringProperty(required= True)
    startDate = ndb.DateProperty(auto_now_add=True)
    roughEstimate = ndb.FloatProperty()
    priority = ndb.IntegerProperty()
    status = ndb.StringProperty()
    
    def set(self):
        return self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    def get(self,id):
        res = ndb.Key(ProductBacklog,int(id)).get()
        return res
    def delete_entity(self,id):
        ndb.Key(ProductBacklog, int(id)).delete()
    
