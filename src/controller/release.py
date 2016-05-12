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
from model.user import Permissions ,OurUser , Groups
import model
from google.appengine.api import users
from webapp2_extras.appengine.auth.models import User
from model import project
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2
import email
from datetime import datetime

class Release(BaseHandler):
    def get(self,*args,**kargs):
        if check_permission(self):
            
           # company=model.user.Tenant()
          #  company_data=company().query(user.OurUser.tenant_domain == kargs['subdomain']).fetch()
           
            u=user.OurUser()
            user1=u.query(user.OurUser.tenant_domain==kargs['subdomain']).get()
           # roles=role.query(ndb.OR(model.user.Groups.tenant_domain==None,model.user.Groups.tenant_domain=='team-google')).fetch()
          #  projmodel=project.Project()
          #  user1=projmodel.query(user.OurUser.tenant_domain==kargs['subdomain']).fetch()
            
            projmodel=project.Project()
            proj=projmodel.get_all()
            
            self.render_template("release.html",{"project":proj,"company_data":user1})
        else:
            self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        release_obj= project.ProjectRelease()
            
        release_obj.projectid= ndb.Key(urlsafe=self.request.get('proj_name'))
           
            
        release_obj.releaseName=self.request.get('release_name')
        release_obj.releaseDate=datetime.strptime(self.request.get('release_date'), '%d/%m/%Y').date()
            
        currentUser=self.auth.get_user_by_session()
        companyId=self.user_model.get_by_id(currentUser['user_id']).tenant_key
        release_obj.companyid = companyId.id()
            
        release_obj.put()
            
        self.redirect('/dashboard')
