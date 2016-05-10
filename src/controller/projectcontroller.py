from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
import logging
import os.path
import webapp2
import time
from model import user
from model import project
import webapp2_extras.appengine.auth.models as auth_user
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import mail
from webapp2_extras import security
from login import BaseHandler,check_permission
from google.appengine.ext import ndb
from datetime import datetime
import json

class ProjectManagement(BaseHandler):
    def get(self,*args,**kargs):
        if check_permission(self):
            projmodel=project.Project()
            proj=projmodel.get_all()
            currentUser=self.auth.get_user_by_session()
            usermodel = user.OurUser().query(user.OurUser.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key)
            self.render_template("user_new/apm-all-projects.html",{"project":proj})
            #self.render_template("user_new/apm-add-project.html")
           
        else:
            #self.response.write("you are not allowed")
            #self.render_template("apm-add-project.html",{'not_permitted':'You are not authorized to view this page'})    
            self.render_template("user_new/apm-all-projects.html")


class AddProjectView(BaseHandler):
    def get(self,*args,**kargs):
        if check_permission(self):
            projmodel=project.Project()
            proj=projmodel.get_all()
            currentUser=self.auth.get_user_by_session()
            usermodel = user.OurUser().query(user.OurUser.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key)
            self.render_template("user_new/apm-add-project.html",{"project":proj,"userslist":usermodel,'permission':'success'})
            #self.render_template("user_new/apm-add-project.html")
           
        else:
            #self.response.write("you are not allowed")
            #self.render_template("apm-add-project.html",{'not_permitted':'You are not authorized to view this page'})    
            self.render_template("user_new/apm-add-project.html")       
        
class AddProject(BaseHandler):
        
    
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        currentUser=self.auth.get_user_by_session()
        companyId=self.user_model.get_by_id(currentUser['user_id']).tenant_key
        logging.info(currentUser)
        logging.info(companyId)
        logging.info(self.request.get("proj_start"))
        projec=project.Project()
        projec.companyid = companyId.id()
        projec.name = self.request.get("proj_name")
        projec.description = self.request.get("proj_desc")
        projec.startDate = datetime.strptime(self.request.get("proj_start"), '%d/%m/%Y').date()
        projec.endDate = datetime.strptime(self.request.get("proj_end"), '%d/%m/%Y').date()
        #projec.team = (self.request.get("proj_team")).split(",")
        projkey = projec.set()
        #logging.info(projkey)
        estimation = project.Estimation()
        estimation.projectid=projkey.id()
        estimation.companyid = companyId.id()
        estimation.estimationLevel="Very Simple"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey.id()
        estimation.companyid = companyId.id()
        estimation.estimationLevel="Simple"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey.id()
        estimation.companyid = companyId.id()
        estimation.estimationLevel ="Medium"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey.id()
        estimation.companyid = companyId.id()
        estimation.estimationLevel="Complex"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey.id()
        estimation.companyid = companyId.id()
        estimation.estimationLevel="Very Complex"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        projemem = project.ProjectMembers()
        projemem.userName =  self.user_model.get_by_id(currentUser['user_id']).name
        projemem.projectid = projkey.id()
        projemem.companyid = companyId.id()
        projemem.userid =   currentUser['user_id']
        projemem.userRole = "Product Owner"
        projemem.set()
        
        self.response.write(projkey.id())
        
class EditProj(BaseHandler):
        
    
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projkey = ndb.Key('Project',int(self.request.get("projid")))
        projec =  projkey.get()
        projec.name = self.request.get("proj_name")
        projec.description = self.request.get("proj_desc")
        projec.startDate = datetime.strptime(self.request.get("proj_start"), '%d/%m/%Y').date()
        projec.endDate = datetime.strptime(self.request.get("proj_end"), '%d/%m/%Y').date()
        #projec.team = (self.request.get("proj_team")).split(",")
        projkey = projec.set()
        
        self.response.write(projkey.id())
                
class AddProjectMembers(BaseHandler):
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        logging.info("it is here "+self.request.__str__())
        userid = self.request.get("userid")
        projid = self.request.get("projid")
        role   = self.request.get("role")
        logging.info("it is here and the userId is"+userid)
        logging.info("it is here and the projid is"+projid)
        logging.info("it is here and the role is"+role)
        
        companyId= self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        projemem = project.ProjectMembers()
        userkey = ndb.Key('OurUser',int(userid))
        model = userkey.get()
        projemem.userName =  model.name
        projemem.projectid = int(projid)
        projemem.companyid = companyId.id()
        projemem.userid =    int(userid)
        projemem.userRole = role
        projekey = projemem.set()
        projmodel = projekey.get()
        
        data = {}
        data['id'] = projmodel.key.id()
        data['projectid'] = projmodel.projectid
        data['companyid'] = projmodel.companyid
        data['userName'] = projmodel.userName
        data['userid'] = projmodel.userid
        data['userRole'] = projmodel.userRole
        
        self.response.write(json.dumps(data, ensure_ascii=False))

class EditProjMem(BaseHandler):
        
    
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projkey = ndb.Key('ProjectMembers',int(self.request.get("userid")))
        projemem =  projkey.get()
        projemem.userRole = self.request.get("role")
        #projec.team = (self.request.get("proj_team")).split(",")
        projmemkey = projemem.set()
        projmemmodel = projmemkey.get()
        data = {}
        data['id'] = projmemmodel.key.id()
        data['projectid'] = projmemmodel.projectid
        data['companyid'] = projmemmodel.companyid
        data['userName'] = projmemmodel.userName
        data['userid'] = projmemmodel.userid
        data['userRole'] = projmemmodel.userRole
        
        self.response.write(json.dumps(data, ensure_ascii=False))
        
        
class AddProjectEstimates(BaseHandler):
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        logging.info("it is here "+self.request.__str__())
        complexity = self.request.get("complexity")
        points = self.request.get("points")
        efforts   = self.request.get("efforts")
        projid = self.request.get("projid")
        logging.info("it is here and the userId is"+complexity)
        logging.info("it is here and the projid is"+points)
        logging.info("it is here and the role is"+efforts)
        
        companyId= self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        estimation = project.Estimation()
        estimation.projectid=int(projid)
        estimation.companyid = companyId.id()
        estimation.estimationLevel=  complexity
        estimation.estimationPoint= int(points)
        estimation.estimationHours= float(efforts)
        estimateskey = estimation.set()
        
        estimatesmodel = estimateskey.get()
        
        data = {}
        data['id'] = estimatesmodel.key.id()
        data['projectid'] = estimatesmodel.projectid
        data['companyid'] = estimatesmodel.companyid
        data['estimationLevel'] = estimatesmodel.estimationLevel
        data['estimationPoint'] = estimatesmodel.estimationPoint
        data['estimationHours'] = estimatesmodel.estimationHours
        
        self.response.write(json.dumps(data, ensure_ascii=False))


class DeleteProject(BaseHandler):
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projid = self.request.get("id")
        proj = project.Project()
        proj.delete_entity(projid)
        self.response.write("success")
        
class DeleteProjectMember(BaseHandler):
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projmemid = self.request.get("id")
        projmem = project.ProjectMembers()
        projmem.delete_entity(projmemid)
        self.response.write("success")
        
class DeleteEstimates(BaseHandler):
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        estimatesid = self.request.get("id")
        esti = project.Estimation()
        esti.delete_entity(estimatesid)
        self.response.write("success")
        
class ViewProject(BaseHandler):
    def get(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        logging.info("it is here proj "+self.request.get("proj_id"))
        projkey = int(self.request.get("proj_id"))
        projmodel=project.Project()
        proj=projmodel.get_proj(projkey)
        
        #proj.startDate = proj.startDate.strftime('%d/%m/%Y')
        #proj.endDate =   proj.endDate.strftime('%d/%m/%Y')
        logging.info("it is here proj "+proj.__str__())
        
        estimationmodel = project.Estimation()
        esti = estimationmodel.get_all(projkey)
        
        projectmembermodel = project.ProjectMembers()
        projmem = projectmembermodel.get_all(projkey)
        
        groupmodel = user.Groups().query(user.Groups.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key)
        
        currentUser=self.auth.get_user_by_session()
        usermodel = user.OurUser().query(user.OurUser.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key)
        self.render_template("user_new/viewproject.html",{"project":proj,"userslist":usermodel,'estimation':esti,'projmem':projmem,'roles':groupmodel})
        
        
class GetTeamMembersForProject(BaseHandler):
    def get(self,*args,**kargs):
       
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project = projectkey.get()
        
        self.render_template("viewteammembers.html",{"project":project})
        
class EditProject(BaseHandler):
    def get(self,*args,**kargs):
       
      
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project_list = projectkey.get()
        
   
        logging.info("test")
        estimation = project.Estimation()
        esti = estimation.query(project.Estimation.projectid == projectkey ).fetch()
        
        logging.info(esti)
        
        self.render_template("editproject.html",{"project":project_list,"estimation":esti})