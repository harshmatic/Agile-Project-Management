import controller.user
import webapp2
from controller.login import *
from controller.admin import *
from controller.user import *
from controller.sprint import *
from controller.projectcontroller import *
from controller.product_backlog_controller import *
from controller.timesheet import *
from controller.release import *
from controller.mytasks import *
from controller.timelog import *
from controller.email_handler import *
from controller.testuserdashboard import *
from controller.effort_estimation_controller import *
from controller.email import *
from webapp2_extras import routes
from webapp2_extras.routes import DomainRoute
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.template import render

def NotFoundPageHandler(request, response, exception):
    
    path = os.path.join(os.path.dirname(__file__), 'view/404.html')
    response.out.write(render(path,{}))



    
app = webapp2.WSGIApplication([
    DomainRoute('<subdomain>.'+APP_DOMAIN, [
                                                        
        #General
        webapp2.Route('/', Main, name='subdomain-home'),
        webapp2.Route('/dashboard', EndUserDashboardHandler, name='dashboard'),          
        webapp2.Route(' /sprint_chart', SprintChart),                 
        webapp2.Route('/login', LoginHandler, name='login'),
        webapp2.Route('/signupadmin', SignupAdminHandler, name='signupadmin'),
        webapp2.Route('/logout', LogoutHandler, name='logout'),
        webapp2.Route('/profile', EndUserProfile,name='profile'),
        webapp2.Route('/profile', EndUserProfile),
        webapp2.Route('/img', EndUserProfile),
        webapp2.Route('/view_photo', UserViewPhotoHandler),
        webapp2.Route('/resource_workload', ResourceWorkload),
        
        #Admin
        webapp2.Route('/admin/signup', SignupHandler, name='adminsignup'),
        webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
        webapp2.Route('/admin/permissions', EditPermissions, name='permissions'),
        webapp2.Route('/admin/editpermission', EditPermission, name='editpaermission'),
        webapp2.Route('/admin/addpermissions', AddPermissions, name='addpermission'),
        webapp2.Route('/admin/addrole', AddRole, name='adrole'),
        webapp2.Route('/admin/editrole', EditRole, name='editrole'),
       
        webapp2.Route('/admin/test_permission', GetPermissions),
        webapp2.Route('/admin/delete', DeleteEntity, name='delete'),
        webapp2.Route('/admin', AdminHome,name="admindashboard"),
        webapp2.Route('/admin/dashboard', AdminHome,name="admindashboard"),
        webapp2.Route('/admin/usermanagment', AdminUserManagement, name='usermanage'),
        webapp2.Route('/admin/verify', AdminVerify, name='verify'),
        webapp2.Route('/admin/view_photo', ViewPhotoHandler,name='viewphoto'),
        webapp2.Route('/admin/edit', AdminEditUser),
        webapp2.Route('/admin/deleteuser', AdminDeleteUser),
        webapp2.Route('/admin/profile', AdminProfile,name='profile'),
        
        #Project
        webapp2.Route('/project/viewmembers', GetTeamMembersForProject,name='viewmebers'),
        webapp2.Route('/project/addproject', AddProject,name='addproject'),
        webapp2.Route('/project/editproject', EditProject,name='editproject'),
        webapp2.Route('/project', ProjectManagement,name='project'),
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
        
        #Backlog
        webapp2.Route('/backlog/addbacklog', AddBacklog,name='addbackloog'),
        webapp2.Route('/backlog', AllBacklogs,name='getbacklog'),
        webapp2.Route('/backlog/getbacklog', Backlog,name='getbacklog'),
        webapp2.Route('/backlog/deletebacklog', DeleteBacklog,name='deletebacklog'),
        webapp2.Route('/backlog/edit', EditBacklog),
        webapp2.Route('/backlog/delete', DeleteBacklog),
        webapp2.Route('/backlog/update', UpdateBacklog),
        
        #webapp2.Route('/get_userStory', GetUserStory),
        webapp2.Route('/dropdown_userstory', GetUserStory),
        #Release
        webapp2.Route('/release', Release,name='release'),
        webapp2.Route('/release/edit', EditRelease),
        webapp2.Route('/release/delete', DeleteRelease),
        webapp2.Route('/release_info', ReleaseInfo),
        
        #Sprint
        webapp2.Route('/sprint', Sprint,name='sprint'),
        webapp2.Route('/sprint/edit', EditSprint),                
        webapp2.Route('/sprint/delete', DeleteSprint),
        webapp2.Route('/sprint_info', SprintInfo),
        webapp2.Route('/sprints/dd', SprintDD, name="sprint_dd"),
        webapp2.Route('/sprint/status', SprintStatus),
       # webapp2.Route('/sprint/sprintstatus', SprintStatus),
        webapp2.Route('/sprint/tasklist', PendingTaskList),
        webapp2.Route('/sprint/pie_chart', SprintPieChart),
       
        
        #Task
        webapp2.Route('/task', Tasks,name='Task'),
        webapp2.Route('/task/addtask', Tasks,name='addTask'),
        webapp2.Route('/task/edittask', EditTask,name='editTask'),
        webapp2.Route('/task/deletetask', DeleteTask),
        webapp2.Route('/task/movetask', MoveTask),
        
        #MyTasks
        webapp2.Route('/mytasks', MyTasks,name='MyTasks'),
        webapp2.Route('/mytasks/view', MyTaskView,name='MyTaskView'),
        webapp2.Route('/mytasks/comment', Comment,name='Comment'),
        
      #  webapp2.Route('/mytask/timelog',Timelog),
        
        webapp2.Route('/timelog/edit', EditTimelog),
        webapp2.Route('/timelog/delete', DeleteTimelog),
        webapp2.Route('/timelog/add', AddTimelog), 
        #Timesheet
        webapp2.Route('/timesheet', Timesheet,name='Timesheet'),
        
        webapp2.Route('/setsession', SetSessionProject),
        
        #Effort Estimation
        webapp2.Route('/efforts', EffortEstimationView,name='estimationView'), 
        webapp2.Route('/efforts/chart', EffortsChart),
       
        webapp2.Route('/efforts/edit', EditEffortEstimation),
        
        webapp2.Route('/test', TestUserDashboard),
        webapp2.Route('/task/status', TaskStatusUpdate),
        
        webapp2.Route('/barchart', Barchart),
        webapp2.Route('/uchart', Utilizationchart),
        webapp2.Route('/velchart', Velocitychart),
        
        #to change all the saved email address to lower
      #  webapp2.Route('/change_email', ChangeEmail)
        
    ]),
        webapp2.Route('/', SignupUser, name='home'),
        webapp2.Route('/email', EmailHandler),
        webapp2.Route('/effortspersist', PersistDefaulEstimation),
        webapp2.Route('/newusereffortspersist', NewUserPersistDefaulEstimation),
        webapp2.Route('/deleteusereffortspersist', DeleteUserPersistDefaulEstimation),
        webapp2.Route('/signupuser', SignupUser, name='signuphome'),
        webapp2.Route('/sprint', Sprint,name='sprint'),
        webapp2.Route('/checkdomain', CheckDomain,name="checkdomain"),
        webapp2.Route('/checkuser', UserEmailInfo),
        webapp2.Route('/basehtml', BaseHtml,name="basehtml"),
        webapp2.Route('/userbasehtml', UserBaseHtml,name="userbasehtml"),
        webapp2.Route('/basehtmltest', BaseHtmlTest,name="basehtmltest"),
        webapp2.Route('/userbasehtmltest', UserBaseHtmlTest,name="userbasehtmltest"),
        webapp2.Route('/login', LoginBaseHandler, name='loginbase'),
        webapp2.Route('/loginhome',LoginHome, name='loginhome'),
        webapp2.Route('/logout', LogoutHandler, name='logout'),
        webapp2.Route('/password', SetPasswordHandler, name="setpassword"),
        webapp2.Route('/signupuser', SignupUser, name='usersignup'),
        webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler=VerificationHandler, name='verification'),
        webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot')
    
], debug=True, config=config)

#app.error_handlers[404] = NotFoundPageHandler
#app.error_handlers[500] = NotFoundPageHandler
