from google.appengine.ext import ndb

from model.user import *

class Project(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    #team = ndb.StringProperty(repeated=True)
    companyid = ndb.IntegerProperty(required=True)
    
    def set(self):
        return self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    def get_proj(self,projid):
        projKey = ndb.Key('Project',projid)
        res = projKey.get()
        return res
    def delete_entity(self,projid):
        ndb.Key(Project, int(projid)).delete()
    
class Estimation(ndb.Model):
    projectid =        ndb.IntegerProperty(required=True)
    companyid =       ndb.IntegerProperty(required=True)
    estimationLevel = ndb.StringProperty(required=True)
    estimationPoint = ndb.IntegerProperty(required=True)
    estimationHours = ndb.FloatProperty(required=True)
    
    def set(self):
        return self.put()
    def get_all(self,projId):
        res = self.query(Estimation.projectid == projId).fetch()
        return res
    def delete_entity(self,estid):
        ndb.Key(Estimation, int(estid)).delete()
    
class ProjectMembers(ndb.Model):
    projectid =        ndb.IntegerProperty(required=True)
    companyid =       ndb.IntegerProperty(required=True)
    userName = ndb.StringProperty(required=True)
    userid   = ndb.IntegerProperty(required=True)
    userRole = ndb.StringProperty(required=True)
    
    def set(self):
        return self.put()
    def get_all(self,projId):
        res = self.query(ProjectMembers.projectid == projId).fetch()
        return res
    def delete_entity(self,projmemid):
        ndb.Key(ProjectMembers, int(projmemid)).delete()
        
class ProjectRelease(ndb.Model):
    projectid =        ndb.IntegerProperty(required=True)
    companyid =       ndb.IntegerProperty(required=True)
    releaseName = ndb.StringProperty(required=True)
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    releaseStartDate = ndb.DateProperty()
    releaseEndDate = ndb.DateProperty()
    
    def set(self):
        return self.put()
    def get_all(self,projId):
        res = self.query(ProjectRelease.projectid == projId).fetch()
        return res
    def delete_entity(self,releaseid):
        ndb.Key(ProjectRelease, int(releaseid)).delete()