from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
import logging
import os.path
import webapp2
import time
from model import user
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
        projmodel=user.Project()
        proj=projmodel.get_all()
        usermodel = user.OurUser().get_all()
        self.render_template("project-management-new.html",{"project":proj,"userslist":usermodel})
        
class AddProject(BaseHandler):
        
    
    def post(self):
        logging.info("it is here "+self.request.__str__())
        project=user.Project()
        project.name = self.request.get("proj_name")
        project.description = self.request.get("proj_desc")
        project.startDate = datetime.strptime(self.request.get("proj_start"), '%d/%m/%Y').date()
        project.endDate = datetime.strptime(self.request.get("proj_end"), '%d/%m/%Y').date()
        project.team = (self.request.get("proj_team")).split(",")
        project.set()
        self.response.write("true")
        
class GetTeamMembersForProject(BaseHandler):
    def get(self):
       
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project = projectkey.get()
        
        self.render_template("viewteammembers.html",{"project":project})