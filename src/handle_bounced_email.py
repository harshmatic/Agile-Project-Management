import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import BounceNotification
from google.appengine.ext.webapp.mail_handlers import BounceNotificationHandler
from google.appengine.api import mail
app = webapp2.WSGIApplication([
    ('/_ah/bounce', LogBounceHandler)], debug=True)

class LogBounceHandler(BounceNotificationHandler):
    def receive(self, bounce_message):
        mail.send_mail(to='harshmatic@gmail.com', sender='harshmatic@gmail.com', subject='Bounced email',
                       body=str(self.request))
        logging.info('Received bounce post ... [%s]', self.request)
        logging.info('Bounce original: %s', bounce_message.original)
        logging.info('Bounce notification: %s', bounce_message.notification)