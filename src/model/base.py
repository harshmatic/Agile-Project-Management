from google.appengine.ext import ndb

class BaseClass(ndb.Model):
    created_by = ndb.StringProperty()
    created_date= ndb.DateTimeProperty(auto_now_add=True)
    modified_by = ndb.StringProperty()
    modified_date =  ndb.DateTimeProperty()
    status =ndb.StringProperty()
    