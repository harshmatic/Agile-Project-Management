from google.appengine.ext import ndb
import logging
from model import user
from login import BaseHandler,check_permission
#import simplejson as json
import json as json
from model import task

from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import webapp2

class Sprint(BaseHandler):
    
    def get(self,*args,**kargs):
        #if check_permission(self):
            types_task=task.Type().get_all()
            self.render_template("user_new/apm-sprint-items.html",{"type":types_task})
        #else:
            #self.response.write("you are not allowed")
    
    def post(self,*args,**kargs):
        key = ndb.Key(urlsafe=self.request.get('key_user'))
        user=key.get()
        if not user.verified:
            user.verified=True
            password=user.name+user.empid
            user.put()
            self.response.write("true"+password)
        else:
            self.response.write("User is already verified.")