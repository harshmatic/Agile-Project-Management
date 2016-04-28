import webapp2
from controller.login import *
from controller.admin import *
from controller.user import *


app = webapp2.WSGIApplication([
    webapp2.Route('/dashboard', EndUserDashboardHandler, name="dashboard"),                           
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/signupadmin', SignupAdminHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/', Main, name='home'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    #webapp2.Route('/permission', AddPermission, name='permission'),
    webapp2.Route('/role', AddRole, name='role'),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    webapp2.Route('/admin/editpermissions', EditPermissions),
    webapp2.Route('/admin/editpermission', EditPermission),
    webapp2.Route('/admin/addpermissions', AddPermissions),
    webapp2.Route('/admin/addrole', AddRole),
    webapp2.Route('/admin/editrole', EditRole),
    webapp2.Route('/admin/delete', DeleteEntity),
    webapp2.Route('/admin/dashboard', AdminHome,name="admindashboard"),
    webapp2.Route('/admin/usermanagment', AdminUserManagement),
    webapp2.Route('/project', ProjectManagementHandler)
    #webapp2.Route('/admin/dasboard', AdminHome)
], debug=True, config=config)
