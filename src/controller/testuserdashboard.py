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
       # if check_permission(self):
            projectKey=self.session['current_project']
            currentUser=self.auth.get_user_by_session()
            currentUser=self.user_model.get_by_id(currentUser['user_id']).key
            project_member=project.ProjectMembers().get_by_project_user(projectKey,currentUser)
            tasks=task.Task().get_by_project_user(projectKey,project_member[0])
            
            open_count=0
            inprogress_count =0
            completed_count=0
            for i in tasks:
                if i.task_status == 'Open':
                    open_count=open_count+1
                if i.task_status == 'In Progress':
                    inprogress_count=inprogress_count+1
                if i.task_status == 'Done':
                    completed_count=completed_count+1   
            

            
            self.render_template("user_new/test.html",{"tasks":tasks,"open_count":open_count,"inprogress_count":inprogress_count,"completed_count":completed_count})
       # else:
           # self.response.write("you are not allowed")
            
            
    