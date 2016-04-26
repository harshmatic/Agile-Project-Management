from google.appengine.ext import ndb
from google.appengine.ext import db
import __builtin__
from model.project import *
import logging
import time
import webapp2_extras.appengine.auth.models as auth_user
from webapp2_extras import security

class OurUser(auth_user.User):
    role = ndb.KeyProperty()
    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)
    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
    # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None
    def get_all(self):
        res = self.query().fetch()
        return res  

class Permissions(ndb.Model):
    url = ndb.StringProperty(required=True)
    permission = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    def set(self):
        self.put()
    def get_all(self):
        res = self.query().fetch()
        return res

        
class Groups(ndb.Model):
    role=ndb.StringProperty(required=True)
    permissions=ndb.KeyProperty(Permissions,repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    def set(self):
        self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    def get(self,**keyargs):
        group =Groups()
        logging.info(keyargs)
        for k, v in keyargs.iteritems():
            setattr(self,k,v)
        qry = Groups.query()
       # qry = self.query(self.role=)
        logging.info(qry)
        return qry