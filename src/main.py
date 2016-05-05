import webapp2
from controller.login import *
from controller.admin import *
from controller.user import *
from controller.projectcontroller import *
from webapp2_extras import routes
from webapp2_extras.routes import DomainRoute

app = webapp2.WSGIApplication([
    DomainRoute('<subdomain>.<version>.apm-eternus.appspot.com', [
        webapp2.Route('/', handler=Main, name='subdomain-home'),
        webapp2.Route('/dashboard', EndUserDashboardHandler, name='dashboard'),                           
        webapp2.Route('/admin/signup', SignupHandler, name='adminsignup'),
        webapp2.Route('/signupadmin', SignupAdminHandler, name='signupadmin'),
        webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification'),
        webapp2.Route('/password', SetPasswordHandler, name="setpassword"),
        webapp2.Route('/login', LoginHandler, name='login'),
        webapp2.Route('/signupuser', SignupUser, name='usersignup'),
        webapp2.Route('/role', AddRole, name='role'),
        webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
        webapp2.Route('/admin/permissions', EditPermissions, name='permissions'),
        webapp2.Route('/admin/editpermission', EditPermission, name='editpaermission'),
        webapp2.Route('/admin/addpermissions', AddPermissions, name='addpermission'),
        webapp2.Route('/admin/addrole', AddRole, name='adrole'),
        webapp2.Route('/admin/editrole', EditRole, name='editrole'),
        webapp2.Route('/admin/delete', DeleteEntity, name='delete'),
        webapp2.Route('/admin', AdminHome,name="admindashboard"),
        webapp2.Route('/admin/dashboard', AdminHome,name="admindashboard"),
        webapp2.Route('/admin/usermanagment', AdminUserManagement, name='usermanage'),
        webapp2.Route('/admin/verify', AdminVerify, name='verify'),
        webapp2.Route('/project/viewmembers', GetTeamMembersForProject,name='viewmebers'),
        webapp2.Route('/project/addproject', AddProject,name='addproject'),
        webapp2.Route('/project/editproject', EditProject,name='editproject'), 
        webapp2.Route('/admin/upload_photo', PhotoUploadHandler,name='photoupload'),
        webapp2.Route('/project', ProjectManagement,name='project'),
        webapp2.Route('/admin/view_photo', ViewPhotoHandler,name='viewphoto'),
        webapp2.Route('/logout', LogoutHandler, name='logout'),
        webapp2.Route('/profile', EndUserProfile,name='profile')
        
    ]),
        webapp2.Route('/login', LoginBaseHandler, name='loginbase'),
        webapp2.Route('/logout', LogoutHandler, name='logout'),
        webapp2.Route('/', SignupUser, name='home'),
        webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot')
        
    
], debug=True, config=config)
