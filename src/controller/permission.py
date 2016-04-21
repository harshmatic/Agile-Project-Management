import login
from model import user
import logging
from google.appengine.ext import ndb

class AddPermission(login.BaseHandler):
    def get(self):
        self.render_template("permission.html")
        
    def post(self):
        url=self.request.get("perm")
        permiss=user.Permissions()
        permiss.url=url
        permiss.set()

class AddRole(login.BaseHandler):
    def get(self):
        permiss=user.Permissions()
        list_per=permiss.get_all()
        param = {"perm":list_per}
        self.render_template("role.html",param)
        
    def post(self):
        url=self.request.get_all("permissions")
        logging.info(url)
        for index, item in enumerate(url):
            url[index] = ndb.Key(urlsafe=item)
        #url = [x  for x in url]
        logging.info(url)
        role=self.request.get("role")
        u=user.Groups()
        u.role=role
        u.permissions=url
        logging.info(url)
        u.set()