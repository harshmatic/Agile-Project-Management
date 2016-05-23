from google.appengine.ext import ndb
import logging
from model import user,project
from login import BaseHandler,check_permission
import json as json
from model import sprint,task
from datetime import datetime

class MyTasks(BaseHandler):
    
    def get(self,*args,**kargs):
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        project_member=project.ProjectMembers().get_by_project_user(projectKey,currentUser)
        logging.info(projectKey)
        logging.info(project_member)
        tasks=task.Task().get_by_project_user(projectKey,project_member[0])
        self.render_template("user_new/my_tasks.html",{"tasks":tasks})

class MyTaskView(BaseHandler):
    
    def get(self,*args,**kargs):
        taskKey = ndb.Key(urlsafe=self.request.get('key'))
        task=taskKey.get()
        projectKey=self.session['current_project']
        currentUser=self.auth.get_user_by_session()
        currentUser=self.user_model.get_by_id(currentUser['user_id']).key
        
        self.render_template("user_new/view_task.html",{"task":task})
        
class Comment(BaseHandler):
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        currentUserKey=self.user_model.get_by_id(currentUser['user_id']).key
        taskKey = ndb.Key(urlsafe=self.request.get('key'))
        tasks=taskKey.get()
        comment = task.Comments()
        comment.commnent_by=currentUserKey
        comment.comment=self.request.get('comment')
        comment.created_by = currentUser['email_address']
        comment.status =True
        tasks.comments.append(comment)
        tasks.put()
        self.response.write("true")