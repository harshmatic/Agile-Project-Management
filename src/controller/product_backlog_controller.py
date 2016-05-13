from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
from model import product_backlog
from model import task
from model import project
import json
import logging
import os.path
import webapp2
import time
from login import BaseHandler,check_permission
from model import user
from model import sprint

class AllBacklogs(BaseHandler):
    def get(self,*args,**kargs):
       if check_permission(self):  
        productBacklog = product_backlog.ProductBacklog()
        productBacklog = productBacklog.get_all()
        
        list= []
        
        for pb in productBacklog:
            data = {}
            data['key'] = pb.key.id()
            data['sprintId'] = pb.sprintId
            data['storyDesc'] = pb.storyDesc
            data['roughEstimate'] = pb.roughEstimate
            data['priority'] = pb.priority
            data['status'] = pb.status
            list.append(data)
        
        
        #self.response.headers['Content-Type'] = 'text/plain'
       
        #self.response.write(json.dumps(list, ensure_ascii=False))
        
        type_obj = task.Type()
        type= type_obj.get_all()
        
        projmodel=project.Project()
        proj=projmodel.get_all()
        
        company_name=kargs['subdomain']
        
        sprint_obj=sprint.Sprint()
        sprints=sprint_obj.get_all()
        
        self.render_template("user_new/apm-backlog-new.html",{"productBacklog":productBacklog,"type":type,"project":proj,"sprint":sprints,"company_name":company_name})
       else:
        self.response.write("you are not allowed")   
        
class Backlog(BaseHandler):
    def get(self,*args,**kargs):
        
        id = self.request.get("id")
        productBacklog = product_backlog.ProductBacklog()
        productBacklog = productBacklog.get(id)
        
        data = {}
        data['key'] = productBacklog.key.id()
        data['sprintId'] = productBacklog.sprintId
        data['storyDesc'] = productBacklog.storyDesc
        data['roughEstimate'] = productBacklog.roughEstimate
        data['priority'] = productBacklog.priority
        data['status'] = productBacklog.status
        
        
       
        
        self.response.write(json.dumps(data, ensure_ascii=False))
        
class AddBacklog(BaseHandler):
    
    def post(self,*args,**kargs):
        backlog = product_backlog.ProductBacklog()
       # backlog.sprintId = self.request.get("spId")
        backlog.project_key = ndb.Key(urlsafe=self.request.get("project"))
        
        currentUser=self.auth.get_user_by_session()
        company_key=self.user_model.get_by_id(currentUser['user_id']).tenant_key
         
           
        backlog.company_key = company_key
        
        if (self.request.get('sprint') != 'None'):
            backlog.sprintId=ndb.Key(urlsafe=self.request.get('sprint'))
            
        backlog.type = ndb.Key(urlsafe=self.request.get('type'))
        backlog.storyDesc = self.request.get("description")
        backlog.backlog_name=self.request.get('backlog_name')
        backlog.roughEstimate = float(self.request.get("rough_estimate"))
        backlog.priority = int(self.request.get("priority"))
        backlog.status = "Defined"
        projkey = backlog.set()
        self.response.write('true')
        
class DeleteBacklog(BaseHandler):
    def get(self,*args,**kargs):
        
        id = self.request.get("id")
        pb = product_backlog.ProductBacklog()
        pb.delete_entity(id)
        self.response.write("Deleted")
        
        

class EditBacklog(BaseHandler):
        def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('edit_key'))
            backlog_info=key.get()
          #  logging.info(backlog_info)
            sprint_obj=sprint.Sprint()
            sprints=sprint_obj.get_all()
            
            projmodel=project.Project()
            proj=projmodel.get_all()
            
            self.render_template("user_new/edit_backlog.html",{"backlog_info":backlog_info,"project":proj,"sprint":sprints})

            
            
        def post(self,*args,**kargs):
          
            key= ndb.Key(urlsafe=self.request.get('key'))
            backlog_key=key.get()
            
            backlog_key.type = ndb.Key(urlsafe=self.request.get('type'))
            backlog_key.storyDesc = self.request.get("description")
            backlog_key.backlog_name=self.request.get('backlog_name')
            backlog_key.roughEstimate = float(self.request.get("rough_estimate"))
            backlog_key.priority = int(self.request.get("priority"))
          
            
            backlog_key.put()
                        
            self.response.write("true")        
