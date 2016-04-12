import os
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
from model.user import User


class Main(webapp2.RequestHandler):
    def get(self):
        tmpl = os.path.join(os.path.dirname(__file__), '../view/main.html')
        self.response.write(render(tmpl, {}))