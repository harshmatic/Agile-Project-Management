import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import BounceNotification
from google.appengine.ext.webapp.mail_handlers import BounceNotificationHandler
from google.appengine.api import mail
# app = webapp2.WSGIApplication([
#     ('/_ah/bounce', LogBounceHandler)], debug=True)

class LogBounceHandler(BounceNotificationHandler):
    def receive(self, bounce_message):
        logging.info('Received bounce post ... [%s]', self.request)
        logging.info('Bounce original: %s', bounce_message.original)
        logging.info('Bounce notification: %s', bounce_message.notification)


app = webapp2.WSGIApplication([LogBounceHandler.mapping()], debug=True)