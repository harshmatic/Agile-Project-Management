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
from model import sprint,task,time_log
from google.appengine.api import users
from webapp2_extras.appengine.auth.models import User
from model import project
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2
import email
from datetime import datetime


class TestUserDashboard(BaseHandler):from google.appengine.ext.webapp import template
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
from model import sprint,task,time_log
from google.appengine.api import users
from webapp2_extras.appengine.auth.models import User
from model import project
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2
import email
from datetime import datetime
from common import checkdomain

class TestUserDashboard(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
      #  if check_permission(self):
            currentUser=self.auth.get_user_by_session()
            comp_key =  self.user_model.get_by_id(currentUser['user_id']).tenant_key
            currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            
            #sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
            
            
            if not self.session.has_key('current_project'):
                
                projects= model.project.ProjectMembers().get_proj_by_user(comp_key,currentUser)
                if not projects:
                    
                    self.session['current_project']= None
                else:
                    self.session['current_project']=projects[0].projectid
                    
                projectKey=self.session['current_project']
                
            else:
                projectKey=self.session['current_project']
            #currentUser=self.auth.get_user_by_session()
            #currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            
            open_count=0
            inprogress_count =0
            completed_count=0
            
            
            if(projectKey != None):
                #project_member=project.ProjectMembers().get_by_project_user(projectKey,currentUser)
                 
                #if sprint key is present
                if (self.request.get('sprint_key')):
                    sprint_key=ndb.Key(urlsafe=self.request.get('sprint_key'))
                    sprint_info=sprint_key.get()
                    tasks=task.Task().query(task.Task.sprint == sprint_key).fetch()
                    logging.info(tasks)
                    for i in tasks:
                        if i.task_status == 'Open':
                            open_count=open_count+1
                        if i.task_status == 'In Progress':
                            inprogress_count=inprogress_count+1
                        if i.task_status == 'Completed':
                            completed_count=completed_count+1  
                    
                    self.render_template("user_new/test.html",{"tasks":tasks,"open_count":open_count,"inprogress_count":inprogress_count,"completed_count":completed_count,"sprint_name":sprint_info.name})
                
                #if sprint key is not there 
                else:
                    tasks=task.Task().get_by_project_user(projectKey,currentUser)
                
                    
                    for i in tasks:
                        if i.task_status == 'Open':
                            open_count=open_count+1
                        if i.task_status == 'In Progress':
                            inprogress_count=inprogress_count+1
                        if i.task_status == 'Completed':
                            completed_count=completed_count+1  
                    self.render_template("user_new/test.html",{"tasks":tasks,"open_count":open_count,"inprogress_count":inprogress_count,"completed_count":completed_count})
                
            
            else:
                
                self.render_template("user_new/test.html",{"tasks":None,"open_count":0,"inprogress_count":0,"completed_count":0})
      #  else:
       #     self.response.write("you are not allowed")