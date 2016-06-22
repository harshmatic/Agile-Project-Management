'''
Created on Jun 22, 2016

@author: Atul Sharma
'''
import logging
def checkdomain(fn):
    def wrapper(self,*args,**kargs):
        logging.info('inside')
        currentUser=self.auth.get_user_by_session()
        logging.info("currentUser")
        logging.info(currentUser)
        if (currentUser != None):
            comp_key =  self.user_model.get_by_id(currentUser['user_id']).tenant_key
            if comp_key.get().domain != self.request.host.split('.')[0]:
                self.redirect('/logout')
            else:
                logging.info('else running')
                return fn(self,*args,**kargs)
        
        else:
            self.redirect('/login')
    return wrapper