from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
from model import product_backlog
import json
import logging
import os.path
import webapp2
import time
from login import BaseHandler,check_permission


class AllBacklogs(BaseHandler):
    def get(self):
        
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
        self.response.write(json.dumps(list, ensure_ascii=False))
        
class Backlog(BaseHandler):
    def get(self):
        
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
    
    def get(self):
        backlog = product_backlog.ProductBacklog()
        backlog.sprintId = self.request.get("spId")
        backlog.storyDesc = self.request.get("spD")
        backlog.roughEstimate = float(self.request.get("rE"))
        backlog.priority = int(self.request.get("priority"))
        backlog.status = self.request.get("status")
        projkey = backlog.set()
        self.response.write(projkey)
        
class DeleteBacklog(BaseHandler):
    def get(self):
        
        id = self.request.get("id")
        pb = product_backlog.ProductBacklog()
        pb.delete_entity(id)
        self.response.write("Deleted")
        
        
        
    
