from google.appengine.api import mail,mail_errors
from login import BaseHandler,check_permission
import logging

class EmailHandler(BaseHandler):
    def post(self):
        
        
        email = self.request.get('To_email')
        verification_url=self.request.get('verification_url')
      
        logging.info(email)
        logging.info(verification_url)
        
        msg = self.request.get('message')
     
        message = mail.EmailMessage(sender="support@ner-monty.appspotmail.com",
                            subject="Account Verification")
        message.to = email
        message.body = msg.format(url=verification_url)
        message.send()
        logging.info("mail sent")