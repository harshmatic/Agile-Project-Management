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

class AdminHome(BaseHandler):
    def get(self):
        if check_permission(self):
            self.render_template("admin/admin-dashboard.html")
        else:
            self.response.write("you are not allowed")
        
class AddPermissions(BaseHandler):
    def get(self):
        self.render_template("admin/addpermissions.html")
        
    def post(self):
        url=self.request.get("perm_url")
        name=self.request.get("perm_name")
        permiss=user.Permissions()
        permiss.url=url
        permiss.permission=name
        permiss.set()
        self.response.write("true")

class AddRole(BaseHandler):
    def get(self):
        permiss=user.Permissions()
        list_per=permiss.get_all()
        param = {"perm":list_per}
        self.render_template("admin/addrole.html",param)
        
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
        self.response.write("true")
        
class EditPermissions(BaseHandler):
    def get(self):
        u=user.Groups()
        role=u.get_all()
        p=user.Permissions()
        perm=p.get_all()
        self.render_template("admin/admin-permissions.html",{"perm":perm,"role":role})
    def post(self):
        prev_role=""
        #role=""
        perm=[]
        #p= user.Groups()
        permission=self.request.get_all("permissions")
        permission.sort();
        for index, item in enumerate(permission):
            row=item.split("<!>")
            role1 = ndb.Key(urlsafe=row[1])
            perm1 = ndb.Key(urlsafe=row[0])
            if prev_role==row[1]:
                perm.append(perm1)
            else:
                if index==0:
                    prev_role=row[1]
                    group=role1.get()
                    perm.append(perm1)
                else:
                    group.permissions=perm
                    group.put()
                    
class AdminUserManagement(BaseHandler):
    def get(self):
        user1 =user.OurUser().get_all()
        logging.info(user1)
        self.render_template("admin/user-management.html",{"user1":user1})