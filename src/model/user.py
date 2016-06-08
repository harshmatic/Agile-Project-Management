from google.appengine.ext import ndb
from google.appengine.ext import db
import __builtin__
from model.project import *
import logging
import time
import webapp2_extras.appengine.auth.models as auth_user
from webapp2_extras import security
from base import BaseClass


class Tenant(BaseClass):
    name = ndb.StringProperty(required=True)
    domain = ndb.StringProperty(required=True)
    created_by = ndb.StringProperty()
    
class OurUser(auth_user.User,BaseClass):
    role = ndb.KeyProperty()
    tenant_domain = ndb.StringProperty()
    tenant_key = ndb.KeyProperty(kind=Tenant)
    blob_key=ndb.BlobKeyProperty()
    project_permission = ndb.BooleanProperty()
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
    
    @classmethod
    def _pre_delete_hook(cls, key):
        us=key.get()
        auth_user.Unique.delete_multi(map(lambda s: '%s.auth_id:'  % (cls.__name__)+ s, us.auth_ids))
        
        
        
class Permissions(BaseClass):
    url = ndb.StringProperty(required=True)
    permission = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    parentName = ndb.StringProperty()
    order= ndb.IntegerProperty()
    icon=ndb.StringProperty()
    
    def set(self):
        self.put()
    def get_all(self):
        res = self.query().order(Permissions.order).fetch()
        return res
    def sa_get_all(self):
        res = self.query().fetch()
        return res
    @classmethod
    def _post_delete_hook(cls, key, future):
        groups = Groups.query(Groups.permissions==key).fetch()
        for group in groups:
            group.permissions.remove(key)
            group.put()
        
class Groups(BaseClass):
    role=ndb.StringProperty(required=True)
    permissions=ndb.KeyProperty(kind=Permissions,repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    tenant_domain = ndb.StringProperty()
    tenant_key = ndb.KeyProperty(kind=Tenant)
    application_level=ndb.BooleanProperty()
    
    def set(self):
        self.put()
    def get_all(self):
        res = self.query().fetch()
        return res
    def get_default_role(self):
        res = self.query(ndb.AND(Groups.role== "Product Owner",Groups.tenant_domain== None)).fetch()
        return res
    def get(self,**keyargs):
        group =Groups()
        for k, v in keyargs.iteritems():
            setattr(self,k,v)
        qry = Groups.query()
        return qry
    @classmethod
    def _post_delete_hook(cls, key, future):
        users = OurUser.query(OurUser.role==key).fetch()
        for user in users:
            user.role.remove(key)
            user.put()