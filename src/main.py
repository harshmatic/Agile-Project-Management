import webapp2
from controller.login import *
from controller.admin import *
from controller.user import *
from controller.projectcontroller import *
from webapp2_extras import routes

app = webapp2.WSGIApplication([
    routes.DomainRoute('<subdomain>.apm-eternus.appspot.com', [
        webapp2.Route('/', handler=Main, name='subdomain-home'),
    ]),
    webapp2.Route('/dashboard', EndUserDashboardHandler, name="dashboard"),                           
    webapp2.Route('/admin/signup', SignupHandler),
    webapp2.Route('/signupadmin', SignupAdminHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/', SignupUser, name='home'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/signupuser', SignupUser),
    webapp2.Route('/role', AddRole, name='role'),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    webapp2.Route('/admin/permissions', EditPermissions),
    webapp2.Route('/admin/editpermission', EditPermission),
    webapp2.Route('/admin/addpermissions', AddPermissions),
    webapp2.Route('/admin/addrole', AddRole),
    webapp2.Route('/admin/editrole', EditRole),
    webapp2.Route('/admin/delete', DeleteEntity),
     webapp2.Route('/admin', AdminHome,name="admindashboard"),
    webapp2.Route('/admin/dashboard', AdminHome,name="admindashboard"),
    webapp2.Route('/admin/usermanagment', AdminUserManagement),
    webapp2.Route('/admin/verify', AdminVerify),
    webapp2.Route('/project/viewmembers', GetTeamMembersForProject),
    webapp2.Route('/project/addproject', AddProject),
    webapp2.Route('/project/editproject', EditProject), 
    webapp2.Route('/admin/upload_photo', PhotoUploadHandler),
    webapp2.Route('/project', ProjectManagement),
    webapp2.Route('/admin/view_photo', ViewPhotoHandler),
    webapp2.Route('/profile', EndUserProfile),
    webapp2.Route('/img', EndUserProfile),
    webapp2.Route('/view_photo', UserViewPhotoHandler)
    
], debug=True, config=config)
