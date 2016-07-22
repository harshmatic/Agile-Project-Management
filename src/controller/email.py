from google.appengine.ext import ndb
import logging
from model import user
from login import BaseHandler,check_permission
from common import checkdomain
import json

class ChangeEmail(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        
       # if check_permission(self):
            u=user.OurUser()
            user1=u.query(user.OurUser.tenant_domain==kargs['subdomain']).fetch()
            upper_emails=[]
            for i in user1:
                a=i.auth_ids
               # l = [item for value in a for item in literal_eval(value)]
                l=json.dumps(a)
               # logging.info(a)
                if l.isupper():
                    logging.info(l)
                    upper_emails.append(l)
            
            self.render_template("admin_new/testuser.html",{"upper_emails":upper_emails})
       # else:
        #    self.response.write("you are not allowed")
            
    @checkdomain
    def post(self,*args,**kargs):
        u=user.OurUser()
        user1=u.query(user.OurUser.tenant_domain==kargs['subdomain']).fetch()
        upper_emails=[]
        for i in user1:
            a=i.auth_ids
               # l = [item for value in a for item in literal_eval(value)]
            l=json.dumps(a)
               # logging.info(a)
            if l.isupper():
                logging.info(l)
                email_list=i.key.get()
                email_list.auth_ids = [x.lower() for x in i.auth_ids]
                upper_emails.append(email_list)
                
                logging.info(upper_emails)
        ndb.put_multi(upper_emails)
        
        self.response.write("true") 
        