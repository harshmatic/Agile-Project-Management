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

class ProjectManagement(BaseHandler):
    def get(self):
        if check_permission(self):
            projmodel=project.Project()
            proj=projmodel.get_all()
            usermodel = user.OurUser().get_all()
            self.render_template("project-management-new.html",{"project":proj,"userslist":usermodel,'permission':'success'})
           
        else:
            #self.response.write("you are not allowed")
            self.render_template("project-management-new.html",{'not_permitted':'You are not authorized to view this page'})    



class AddProject(BaseHandler):
        
    
    def post(self):
        logging.info("it is here "+self.request.__str__())
        currentUser=self.auth.get_user_by_session()
        companyId=self.user_model.get_by_id(currentUser['user_id']).tenant_key
        projec=project.Project()
        project.companyid = companyId
        projec.name = self.request.get("proj_name")
        projec.description = self.request.get("proj_desc")
        projec.startDate = datetime.strptime(self.request.get("proj_start"), '%d/%m/%Y').date()
        projec.endDate = datetime.strptime(self.request.get("proj_end"), '%d/%m/%Y').date()
        projec.team = (self.request.get("proj_team")).split(",")
        projkey = projec.set()
        #logging.info(projkey)
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Very Simple"
        estimation.estimationPoint=int(self.request.get("VsPoint"))
        estimation.estimationHours=float(self.request.get("VsHour"))
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Simple"
        estimation.estimationPoint=int(self.request.get("SPoint"))
        estimation.estimationHours=float(self.request.get("SHour"))
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel ="Medium"
        estimation.estimationPoint=int(self.request.get("MPoint"))
        estimation.estimationHours=float(self.request.get("MHour"))
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Complex"
        estimation.estimationPoint=int(self.request.get("CPoint"))
        estimation.estimationHours=float(self.request.get("CHour"))
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Very Complex"
        estimation.estimationPoint=int(self.request.get("VcPoint"))
        estimation.estimationHours=float(self.request.get("VcHour"))
        estimation.set()
        
        self.response.write("true")
        
class GetTeamMembersForProject(BaseHandler):
    def get(self):
       
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project = projectkey.get()
        
        self.render_template("viewteammembers.html",{"project":project})
        
class EditProject(BaseHandler):
    def get(self):
       
      
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project_list = projectkey.get()
        
   
        
        estimation = project.Estimation()
        esti = estimation.query(project.Estimation.projectid == projectkey ).fetch()
        
        logging.info(esti)
        
        self.render_template("editproject.html",{"project":project_list,"estimation":esti})