from google.appengine.ext import ndb

from model.user import *
from base import BaseClass

class Project(BaseClass):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    startDate = ndb.DateProperty()
    endDate = ndb.DateProperty()
    #team = ndb.StringProperty(repeated=True)
    companyid = ndb.KeyProperty(required=True)
    
    def set(self):
        return self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    def get_proj(self,projid):
        projKey = ndb.Key('Project',projid)
        res = projKey.get()
        return res
    def get_proj_by_user(self,comp_id):
        #projKey = ndb.Key('Project',projid)
        res = self.query(Project.companyid==comp_id).fetch()
        return res
    def delete_entity(self,projid):
        ndb.Key(Project, int(projid)).delete()
    
class Estimation(BaseClass):
    projectid =        ndb.KeyProperty(required=True)
    companyid =       ndb.KeyProperty(required=True)
    estimationLevel = ndb.StringProperty(required=True)
    estimationPoint = ndb.IntegerProperty(required=True)
    estimationHours = ndb.FloatProperty(required=True)
    
    def set(self):
        return self.put()
    def get_all(self,projId):
        res = self.query(ndb.AND(Estimation.projectid == projId,Estimation.status == True)).fetch()
        return res
    def delete_entity(self,estid):
        ndb.Key(Estimation, int(estid)).delete()
    
class ProjectMembers(BaseClass):
    projectid = ndb.KeyProperty(required=True)
    roleid = ndb.KeyProperty(required=True)
    companyid = ndb.KeyProperty(required=True)
    userName = ndb.StringProperty(required=True)
    userid   = ndb.KeyProperty(required=True)
    userRole = ndb.StringProperty(required=True)
    
    def set(self):
        return self.put()
    def get_all(self,projId):
        res = self.query(ProjectMembers.projectid == projId).fetch()
        return res
    def get_active(self,projId):
        res = self.query(ndb.AND(ProjectMembers.projectid == projId,ProjectMembers.status == True)).fetch()
        return res
    def delete_entity(self,projmemid):
        ndb.Key(ProjectMembers, int(projmemid)).delete()
    def get_proj_by_user(self,comp_id,user_id):
        res = self.query(ndb.AND(ProjectMembers.companyid==comp_id,ProjectMembers.userid==user_id,ProjectMembers.status == True)).fetch()
        return res
    def get_by_project_user(self,project_id,user_id):
        res = self.query(ndb.AND(ProjectMembers.projectid==project_id,ProjectMembers.userid==user_id)).fetch(keys_only=True)
        return res
        
class ProjectRelease(BaseClass):
    projectid =        ndb.KeyProperty(required=True)
    companyid =       ndb.IntegerProperty(required=True)
    releaseName = ndb.StringProperty(required=True)
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    #releaseStartDate = ndb.DateProperty()
    releaseDate = ndb.DateProperty()
    
    def set(self):
        return self.put()
    def get_all(self,projId):
        res = self.query(ProjectRelease.projectid == projId).fetch()
        return res
    def delete_entity(self,id):
        ndb.Key(ProjectRelease, int(id)).delete()
    def getall(self):
        res = self.query().fetch()
        return res
    def get_by_project(self,projId): 
        return self.query(ProjectRelease.projectid == projId).fetch()