import webapp2
from controller.superadmin import *
from controller.login import *


app = webapp2.WSGIApplication([
    webapp2.Route('/superadmin/dashboard', SuperDashboardHandler),
    webapp2.Route('/superadmin/editpermissions', SuperPermissionsHandler),
    webapp2.Route('/superadmin/signupadmin', SuperSignupAdminHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification')
], debug=True, config=config)
