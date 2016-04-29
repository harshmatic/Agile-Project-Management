import webapp2
from controller.superadmin import *


app = webapp2.WSGIApplication([
    webapp2.Route('/superadmin/dashboard', SuperDashboardHandler),
    webapp2.Route('/superadmin/editpermissions', SuperPermissionsHandler),
    webapp2.Route('/superadmin/signupadmin', SignupAdminHandler)
], debug=True)
