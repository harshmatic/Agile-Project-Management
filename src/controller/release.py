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
from model import project,sprint
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2
import email
from datetime import datetime
from common import checkdomain


class Release(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        #if check_permission(self):
            
           # company=model.user.Tenant()
          #  company_data=company().query(user.OurUser.tenant_domain == kargs['subdomain']).fetch()
           
            u=user.OurUser()
            user1=u.query(user.OurUser.tenant_domain==kargs['subdomain']).get()
           # roles=role.query(ndb.OR(model.user.Groups.tenant_domain==None,model.user.Groups.tenant_domain=='team-google')).fetch()
          #  projmodel=project.Project()
          #  user1=projmodel.query(user.OurUser.tenant_domain==kargs['subdomain']).fetch()
            
            projmodel=project.Project()
            proj=projmodel.get_all()
            company_name=kargs['subdomain']
            
            release_data=project.ProjectRelease()
            release=release_data.getall()
            
            self.render_template("user_new/release.html",{"project":proj,"company_name":company_name,"release":release})
        #else:
            #self.response.write("you are not allowed")
    
    @checkdomain
    def post(self,*args,**kargs):
        release_obj= project.ProjectRelease()
            
       # release_obj.projectid= ndb.Key(urlsafe=self.request.get('proj_name'))
       
        release_obj.projectid= self.session['current_project']   
            
        release_obj.releaseName=self.request.get('release_name')
        release_obj.releaseDate=datetime.strptime(self.request.get('release_date'), '%m/%d/%Y').date()
            
        currentUser=self.auth.get_user_by_session()
        companyId=self.user_model.get_by_id(currentUser['user_id']).tenant_key
        release_obj.companyid = companyId.id()
        
        release_obj.created_by = currentUser['email_address']
        release_obj.status = True
        
            
        release_obj.put()
            
        self.response.write('true')
        


class EditRelease(BaseHandler):
        @checkdomain
        def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('edit_key'))
            release_info=key.get()
            self.render_template("user_new/edit_release.html",{"release_info":release_info})

            
        @checkdomain    
        def post(self,*args,**kargs):
            key= ndb.Key(urlsafe=self.request.get('key'))
            release_key=key.get()
            
            project1 =self.session['current_project']   
            sprint_data=sprint.Sprint().get_by_project(project1)
            
            
            #release_key.projectid= ndb.Key(urlsafe=self.request.get('proj_name'))
          
            release_key.projectid=self.session['current_project'] 
            
            release_key.releaseName=self.request.get('release_name')
            
            release_date=self.request.get('release_date')
            logging.info(release_date)
            
            
            if (release_date != release_key.releaseDate ):
                releaseDate=datetime.strptime(self.request.get('release_date'), '%m/%d/%Y').date()
                
             #   startDate=datetime(0001,01,01)
               # x = datetime.now()
             #   logging.info(x.date())
                endDate=datetime.strptime('01/01/0001','%m/%d/%Y').date()
                
               
                for i in sprint_data:
                 
                    logging.info(i.endDate)
                    logging.info(releaseDate)
                    
                    if (i.endDate != None):  
                        if(i.endDate > endDate):
                        
                            endDate=i.endDate
                            logging.info(endDate)
                    
                
                
                if (endDate > releaseDate):
                       # endDate=i.endDate.strftime('%d/%m/%Y')
                       # a='Cannot be less than'+endDate
                    self.response.write(endDate)
                
                else:
                            release_key.releaseDate=releaseDate
                            user_info = self.auth.get_user_by_session()
                            release_key.modified_by = user_info['email_address']
                            release_key.modified_date = datetime.now()
                            release_key.put()
                            self.response.write('true')

 
class DeleteRelease(BaseHandler):  
        @checkdomain  
        def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('delete_key'))
            release_info = key.get()
            
            self.render_template("user_new/delete_release.html",{"release_info":release_info})
        
        @checkdomain  
        def post(self,*args,**kargs):
            key= ndb.Key(urlsafe=self.request.get('delete_key'))
            release_key=key.get()
         
            user_info = self.auth.get_user_by_session()
            release_key.modified_by = user_info['email_address']
            release_key.modified_date = datetime.now()
            release_key.status = False
           
                  
            release_key.put()
            #user_key.delete()  
            self.response.write("true")     
            
class ReleaseInfo(BaseHandler):
    @checkdomain 
    def post(self,*args,**kargs):
        #if check_permission(self):
           # project = ndb.Key(urlsafe=self.request.get("key"))
            key = ndb.Key(urlsafe=self.request.get('key'))
            release_info=key.get()
           # self.render_template("user_new/delete_sprint.html",{"sprint_info":sprint_info})
            
            endDate = release_info.releaseDate
            endDate=endDate.strftime('%m/%d/%Y')
           
            params=endDate
           
            self.response.write(params)
            
            
