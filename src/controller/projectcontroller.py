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
        estimation.projectid=projkey
        estimation.estimationLevel="Very Simple"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Simple"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel ="Medium"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Complex"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.estimationLevel="Very Complex"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.set()
        
        
        self.response.write("true")
        
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