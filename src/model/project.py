from google.appengine.ext import ndb
from model.user import *

class Projects(ndb.Model):
    project_name=ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    
class ProjectMembersGroup(ndb.Model):
    project_id = ndb.KeyProperty(required=True)
    user_id = ndb.KeyProperty(required=True)
    group_id = ndb.KeyProperty(required=True)
    permissions = ndb.KeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)