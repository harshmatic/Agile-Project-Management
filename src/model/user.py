from google.appengine.ext import ndb
from google.appengine.ext import db
import __builtin__
from model.project import *
import logging

class User(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    designation = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    project_id = ndb.KeyProperty(repeated=True)
    contact_no = ndb.StringProperty()
    emp_id= ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    '''def set(self,**args):
        if 'key' not in args:
            try:
                if args is not None:
                    for key1, value in args.iteritems():
                        setattr( self, key1, value )                
                key_return= self.put()
                return key_return
            except db.Error:
                return False
        else:
            update_key= args['key']
            update_key1=ndb.Key(urlsafe=update_key)
            user = update_key1.get()
            for key1, value in args.iteritems():
                if key1 != 'key':
                    setattr( user, key1, value )
            user.put()
            return update_key1'''
    
    def set(self,**args):
        if 'key' in args:
            k=args['key']
            if User.query(User.key == k).get(keys_only=True) is None:
                raise Exception('Key Not Found')
        else:
            for key1, value in args.iteritems():
                setattr( self, key1, value )
            try:
                key_return=self.put()
                return key_return
            except db.Error():
                return "Something Went Wrong"
    
    @classmethod
    def check(self,email):
        if User.query(User.email == email).get(keys_only=True) is None:
            return False
        else:
            return True
        
        
        
    
class Groups(ndb.Model):
    role=ndb.StringProperty(required=True)
    permissions=ndb.KeyProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
class Permissions(ndb.Model):
    permission = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)