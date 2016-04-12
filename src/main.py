import webapp2
from controller.home import *
from controller.login import *
app = webapp2.WSGIApplication([
    ('/', Main),
    ('/login', Login),
    ('/register', Register)
], debug=True)
