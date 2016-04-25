import login
from model import user
import logging
from google.appengine.ext import ndb

class AddPermission(login.BaseHandler):
    def get(self):
        self.render_template("auth/permission.html")
        
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
        
class EditPermissions(login.BaseHandler):
    def get(self):
        u=user.Groups()
        role=u.get_all()
        p=user.Permissions()
        perm=p.get_all()
        self.render_template("auth/permissions.html",{"perm":perm,"role":role})
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
        
        
        
        
        
        