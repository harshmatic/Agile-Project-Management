import webapp2
from controller.login import *
from controller.admin import *
from controller.user import *
from controller.sprint import *
from controller.projectcontroller import *
from controller.product_backlog_controller import *
from controller.release import *
from webapp2_extras import routes
from webapp2_extras.routes import DomainRoute
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.template import render

def NotFoundPageHandler(request, response, exception):
    
    path = os.path.join(os.path.dirname(__file__), 'view/404.html')
    response.out.write(render(path,{}))
    
app = webapp2.WSGIApplication([
    DomainRoute('<subdomain>.apm-eternus.appspot.com', [
        webapp2.Route('/', Main, name='subdomain-home'),
        webapp2.Route('/dashboard', EndUserDashboardHandler, name='dashboard'),                           
        webapp2.Route('/admin/signup', SignupHandler, name='adminsignup'),
        webapp2.Route('/signupadmin', SignupAdminHandler, name='signupadmin'),
        
        
        webapp2.Route('/login', LoginHandler, name='login'),
        
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
        webapp2.Route('/project', ProjectManagement,name='project'),
        webapp2.Route('/admin/view_photo', ViewPhotoHandler,name='viewphoto'),
        webapp2.Route('/logout', LogoutHandler, name='logout'),
        webapp2.Route('/profile', EndUserProfile,name='profile'),
        webapp2.Route('/backlog/addbacklog', AddBacklog,name='addbackloog'),
        webapp2.Route('/backlog/getallbacklog', AllBacklogs,name='getbacklog'),
        webapp2.Route('/backlog/getbacklog', Backlog,name='getbacklog'),
        webapp2.Route('/backlog/deletebacklog', DeleteBacklog,name='deletebacklg'),
        webapp2.Route('/sprint', Sprint,name='sprint'),
        
        webapp2.Route('/admin/edit', AdminEditUser),
        webapp2.Route('/admin/deleteuser', AdminDeleteUser),
        webapp2.Route('/profile', EndUserProfile),
        webapp2.Route('/img', EndUserProfile),
        webapp2.Route('/view_photo', UserViewPhotoHandler),
        webapp2.Route('/admin/profile', AdminProfile,name='profile'),
        
        webapp2.Route('/project/addnewproject', AddProjectView,name='addnewproject'),
        webapp2.Route('/project/viewproject', ViewProject,name='viewproject'),
        webapp2.Route('/project/addmembertoproj', AddProjectMembers,name='addmembertoproj'),
        webapp2.Route('/project/addestimatetoproj', AddProjectEstimates,name='addestimatetoproj'),
        webapp2.Route('/project/deleteproject', DeleteProject,name='deleteproject'),
        webapp2.Route('/project/deleteMember', DeleteProjectMember,name='deleteMember'),
        webapp2.Route('/project/deleteEstimate', DeleteEstimates,name='deleteEstimate'),
        webapp2.Route('/project/editproj', EditProj,name='editproj'),
        webapp2.Route('/project/editmembertoproj', EditProjMem,name='editestimatetoproj'),
        webapp2.Route('/project/editestimatetoproj', EditEstimates,name='project'),
        webapp2.Route('/project', ProjectManagement,name='project'),
        webapp2.Route('/release', Release,name='release'),
      #  webapp2.Route('/userbasehtml', UserBaseHtml,name="userbasehtml"),
        
    ]),
        webapp2.Route('/sprint', Sprint,name='sprint'),
        webapp2.Route('/checkdomain', CheckDomain,name="checkdomain"),
        webapp2.Route('/basehtml', BaseHtml,name="basehtml"),
        webapp2.Route('/userbasehtml', UserBaseHtml,name="userbasehtml"),
        webapp2.Route('/basehtmltest', BaseHtmlTest,name="basehtmltest"),
        webapp2.Route('/userbasehtmltest', UserBaseHtmlTest,name="userbasehtmltest"),
        webapp2.Route('/login', LoginBaseHandler, name='loginbase'),
        webapp2.Route('/logout', LogoutHandler, name='logout'),
        webapp2.Route('/', SignupUser, name='home'),
        webapp2.Route('/password', SetPasswordHandler, name="setpassword"),
        webapp2.Route('/signupuser', SignupUser, name='usersignup'),
        webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification'),
        webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
        #webapp2.Route('/.*', NotFoundPageHandler)
        webapp2.Route('/release', Release,name='release')
    
], debug=True, config=config)

#app.error_handlers[404] = NotFoundPageHandler
#app.error_handlers[500] = NotFoundPageHandler
