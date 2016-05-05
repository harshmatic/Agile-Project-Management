import webapp2
from controller.superadmin import *
from controller.login import *


app = webapp2.WSGIApplication([
    webapp2.Route('/superadmin', SuperDashboardHandler),
    webapp2.Route('/superadmin/dashboard', SuperDashboardHandler),
    webapp2.Route('/superadmin/permissions', SuperPermissionsHandler),
    webapp2.Route('/superadmin/signupadmin', SuperSignupAdminHandler),
    webapp2.Route('/superadmin/editpermission', SuperEditPermission),
    webapp2.Route('/superadmin/addpermission', SuperAddPermission),
    webapp2.Route('/superadmin/addrole', SuperAddRole),
    webapp2.Route('/superadmin/editrole', SuperEditRole),
    webapp2.Route('/superadmin/usermanagment', SuperUsers),
    webapp2.Route('/superadmin/verify', SuperAdminVerify, name='verify'),
    webapp2.Route('/superadmin/edit', SuperAdminEditUser),
    webapp2.Route('/superadmin/delete', SuperAdminDeleteUser),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification')
], debug=True, config=config)
