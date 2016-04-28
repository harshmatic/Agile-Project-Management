from google.appengine.ext import ndb
import logging
from model import user
from login import BaseHandler,check_permission
#from src.model.user import Groups

class AdminHome(BaseHandler):
    def get(self):
        if check_permission(self):
            self.render_template("admin/admin-dashboard.html")
        else:
            self.response.write("you are not allowed")
class DeleteEntity(BaseHandler):
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key_permission'))
        key.delete()
        #logging.info()
        #q=qry.filter(key in parent)
        #logging.info(qry)
class EditRole(BaseHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        role = key.get()
        permiss=user.Permissions()
        list_per=permiss.get_all()
        self.render_template("admin/editrole.html",{"role":role,"permission":list_per})
        
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key_role'))
        role =key.get()
        role.role=self.request.get("role")
        perm=[]
        array_permissions=self.request.get_all("permissions")
        logging.info(array_permissions)
        for permission in array_permissions:
            perm.append(ndb.Key(urlsafe=permission))
        role.permissions=perm
        role.put()
        self.response.write("true")

class EditPermission(BaseHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        permission = key.get()
        self.render_template("admin/editpermission.html",{"permission":permission})
        
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key_permission'))
        permission =key.get()
        permission.url=self.request.get("url_permission")
        permission.permission=self.request.get("name_permission")
        permission.put()
        self.response.write("true")
        
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
        role=self.request.get("role")
        u=user.Groups()
        u.role=role
        u.permissions=url
        logging.info(url)
        u.put()
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
        permission.sort()
        for index, item in enumerate(permission):
            row=item.split("<!>")
            role1 = ndb.Key(urlsafe=row[0])
            perm1 = ndb.Key(urlsafe=row[1])
            
            if prev_role==row[0]:
                perm.append(perm1)
            else:
                if index !=0:
                    group=ndb.Key(urlsafe=prev_role).get()
                    group.permissions=perm
                    group.put()
                    perm=[]
                    prev_role=row[0]
                    perm.append(perm1)
                else:
                    prev_role=row[0]
                    perm.append(perm1) 
            logging.info(prev_role)
            logging.info(perm)      
            
        self.response.write("true")
                    
class AdminUserManagement(BaseHandler):
    def get(self):
        user1 =user.OurUser().get_all()
        logging.info(user1)
        self.render_template("admin/user-management.html",{"user1":user1})