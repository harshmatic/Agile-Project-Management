from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.ext.webapp.template import render
import logging
import os.path
import webapp2
import time
import model
from model import user
from model import project,sprint
import webapp2_extras.appengine.auth.models as auth_user
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import mail
from webapp2_extras import security
from login import BaseHandler,check_permission
from google.appengine.ext import ndb
from datetime import datetime
import json
from google.appengine.api.taskqueue import taskqueue
from common import checkdomain
from model import task,effort_estimation,product_backlog
 

class ProjectManagement(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        #if check_permission(self):
            projmodel=project.Project()
            projmemmodel = project.ProjectMembers()
            currentUser=self.auth.get_user_by_session()
            #proj=projmodel.get_proj_by_user(self.user_model.get_by_id(currentUser['user_id']).tenant_key)
            projformem = projmemmodel.get_proj_by_user(self.user_model.get_by_id(currentUser['user_id']).tenant_key,self.user_model.get_by_id(currentUser['user_id']).key)
            keys=[]
            for promem in projformem:
                keys.append(promem.projectid)
                
            proj = ndb.get_multi(keys)
                    
            #usermodel = user.OurUser().query(user.OurUser.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key)
            self.render_template("user_new/apm-all-projects.html",{"project":proj})
            #self.render_template("user_new/apm-add-project.html")
           
        #else:
            #self.response.write("you are not allowed")
            #self.render_template("apm-add-project.html",{'not_permitted':'You are not authorized to view this page'})    
            #self.response.write("You have no permissions to access this page")


class AddProjectView(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        if check_permission(self):
            projmodel=project.Project()
            proj=projmodel.get_all()
            currentUser=self.auth.get_user_by_session()
            usermodel = user.OurUser().query(user.OurUser.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key)
            self.render_template("user_new/apm-add-project.html",{"project":proj,"userslist":usermodel,'permission':'success'})
            #self.render_template("user_new/apm-add-project.html")
           
        else:
            #self.response.write("you are not allowed")
            #self.render_template("apm-add-project.html",{'not_permitted':'You are not authorized to view this page'})    
            self.render_template("user_new/apm-add-project.html")       
        
class AddProject(BaseHandler):
        
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        currentUser=self.auth.get_user_by_session()
        companyId=self.user_model.get_by_id(currentUser['user_id']).tenant_key
        logging.info(currentUser)
        logging.info(companyId)
        logging.info(self.request.get("proj_start"))
        projec=project.Project()
        projec.companyid = companyId
        projec.name = self.request.get("proj_name")
        projec.description = self.request.get("proj_desc")
        projec.startDate = datetime.strptime(self.request.get("proj_start"), '%m/%d/%Y').date()
        projec.endDate = datetime.strptime(self.request.get("proj_end"), '%m/%d/%Y').date()
        
        projec.created_by = currentUser['email_address']
        projec.status = True
        #projec.team = (self.request.get("proj_team")).split(",")
        projkey = projec.set()
        #logging.info(projkey)
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.companyid = companyId
        estimation.estimationLevel="Very Simple"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.created_by = currentUser['email_address']
        estimation.status = True
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.companyid = companyId
        estimation.estimationLevel="Simple"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.created_by = currentUser['email_address']
        estimation.status = True
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.companyid = companyId
        estimation.estimationLevel ="Medium"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.created_by = currentUser['email_address']
        estimation.status = True
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.companyid = companyId
        estimation.estimationLevel="Complex"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.created_by = currentUser['email_address']
        estimation.status = True
        estimation.set()
        
        estimation = project.Estimation()
        estimation.projectid=projkey
        estimation.companyid = companyId
        estimation.estimationLevel="Very Complex"
        estimation.estimationPoint= 1
        estimation.estimationHours= 1.0
        estimation.created_by = currentUser['email_address']
        estimation.status = True
        estimation.set()
        
        projemem = project.ProjectMembers()
        projemem.userName =  self.user_model.get_by_id(currentUser['user_id']).name
        projemem.projectid = projkey
        projemem.companyid = companyId
        projemem.userid =   self.user_model.get_by_id(currentUser['user_id']).key
        group = user.Groups()
        groupmodel = group.get_default_role()
        for g in groupmodel:
            projemem.userRole = g.role
            projemem.roleid = g.key
        projemem.created_by = currentUser['email_address']
        projemem.status = True
        projemem.set()
        
        self.response.write(projkey.id())
        
class EditProj(BaseHandler):
        
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projkey = ndb.Key('Project',int(self.request.get("projid")))
        projec =  projkey.get()
        projec.name = self.request.get("proj_name")
        projec.description = self.request.get("proj_desc")
        projec.startDate = datetime.strptime(self.request.get("proj_start"), '%m/%d/%Y').date()
        projec.endDate = datetime.strptime(self.request.get("proj_end"), '%m/%d/%Y').date()
        user_info = self.auth.get_user_by_session()
        projec.modified_by = user_info['email_address']
        projec.modified_date = datetime.now()
        
        #projec.team = (self.request.get("proj_team")).split(",")
        projkey = projec.set()
        
        self.response.write(projkey.id())
                
class AddProjectMembers(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        logging.info("it is here "+self.request.__str__())
        userid = self.request.get("userid")
        projid = self.request.get("projid")
        roleid   = self.request.get("role")
        logging.info("it is here and the userId is"+userid)
        logging.info("it is here and the projid is"+projid)
        logging.info("it is here and the role is"+roleid)
        
        companyId= self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        projemem = project.ProjectMembers()
        userkey = ndb.Key('OurUser',int(userid))
        model = userkey.get()
        projemem.userName =  model.name
        projemem.projectid = ndb.Key('Project',int(projid))
        projemem.companyid = companyId
        projemem.userid =    userkey
        projemem.roleid = ndb.Key('Groups',int(roleid))
        projemem.userRole = ndb.Key('Groups',int(roleid)).get().role
        
        user_info = self.auth.get_user_by_session()
        projemem.created_by = user_info['email_address']
        projemem.status = True
        
        projekey = projemem.set()
        projmodel = projekey.get()
        
        sprints = sprint.Sprint().get_by_project(projmodel.projectid)
        logging.info
        if not sprints:
            logging.info("No sprints")
        else:
            task = taskqueue.add(
            queue_name = "my-push-queue",                 
            url='/newusereffortspersist',
            params={'projectid': projmodel.projectid.id(),'userid':projmodel.userid.id()})
        
        
        data = {}
        data['id'] = projmodel.key.id()
        data['projectid'] = projmodel.projectid.id()
        data['companyid'] = projmodel.companyid.id()
        data['userName'] = (projmodel.userid).get().name
        data['userid'] = projmodel.userid.id()
        data['userRole'] = projmodel.userRole
        
        self.response.write(json.dumps(data, ensure_ascii=False))

class EditProjMem(BaseHandler):
        
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projkey = ndb.Key('ProjectMembers',int(self.request.get("userid")))
        projemem =  projkey.get()
        projemem.userRole = self.request.get("role")
        #projec.team = (self.request.get("proj_team")).split(",")
        user_info = self.auth.get_user_by_session()
        projemem.modified_by = user_info['email_address']
        projemem.modified_date = datetime.now()
        
        projmemkey = projemem.set()
        projmemmodel = projmemkey.get()
        data = {}
        data['id'] = projmemmodel.key.id()
        data['projectid'] = projmemmodel.projectid.id()
        data['companyid'] = projmemmodel.companyid.id()
        data['userName'] = (projmemmodel.userid).get().name
        data['userid'] = projmemmodel.userid.id()
        data['userRole'] = projmemmodel.userRole
        
        self.response.write(json.dumps(data, ensure_ascii=False))

class EditEstimates(BaseHandler):
        
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        estikey = ndb.Key('Estimation',int(self.request.get("estid")))
        logging.info("it is here "+self.request.__str__())
        complexity = self.request.get("complexity")
        points = self.request.get("points")
        efforts   = self.request.get("efforts")
        est =  estikey.get()
        
       
        est.estimationLevel=  complexity
        est.estimationPoint= int(points)
        est.estimationHours= float(efforts)
        
        
        user_info = self.auth.get_user_by_session()
        est.modified_by = user_info['email_address']
        est.modified_date = datetime.now()
        
        estresp = est.set()
        #projec.team = (self.request.get("proj_team")).split(",")
        
        estimatesmodel = estresp.get()
        
        data = {}
        data['id'] = estimatesmodel.key.id()
        data['projectid'] = estimatesmodel.projectid.id()
        data['companyid'] = estimatesmodel.companyid.id()
        data['estimationLevel'] = estimatesmodel.estimationLevel
        data['estimationPoint'] = estimatesmodel.estimationPoint
        data['estimationHours'] = estimatesmodel.estimationHours
        
        self.response.write(json.dumps(data, ensure_ascii=False))
        
        
class AddProjectEstimates(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        logging.info("it is here "+self.request.__str__())
        complexity = self.request.get("complexity")
        points = self.request.get("points")
        efforts   = self.request.get("efforts")
        projid = self.request.get("projid")
        logging.info("it is here and the userId is"+complexity)
        logging.info("it is here and the projid is"+points)
        logging.info("it is here and the role is"+efforts)
        
        companyId= self.user_model.get_by_id(currentUser['user_id']).tenant_key
        
        estimation = project.Estimation()
        estimation.projectid=ndb.Key('Project',int(projid))
        estimation.companyid = companyId
        estimation.estimationLevel=  complexity
        estimation.estimationPoint= int(points)
        estimation.estimationHours= float(efforts)
     
        estimation.created_by = currentUser['email_address']
        estimation.status = True
        
        estimateskey = estimation.set()
        
        estimatesmodel = estimateskey.get()
        
        data = {}
        data['id'] = estimatesmodel.key.id()
        data['projectid'] = estimatesmodel.projectid.id()
        data['companyid'] = estimatesmodel.companyid.id()
        data['estimationLevel'] = estimatesmodel.estimationLevel
        data['estimationPoint'] = estimatesmodel.estimationPoint
        data['estimationHours'] = estimatesmodel.estimationHours
        
        self.response.write(json.dumps(data, ensure_ascii=False))


class DeleteProject(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
            key = ndb.Key(urlsafe=self.request.get('delete_key'))
            project_info = key.get()
            
            self.render_template("user_new/delete_project.html",{"project_info":project_info})
    
    @checkdomain
    def post(self,*args,**kargs):
#        logging.info("it is here "+self.request.__str__())
#        projid = self.request.get("id")
#        proj = project.Project()
#      
#        proj.delete_entity(projid)
#        self.response.write("success")

        key= ndb.Key(urlsafe=self.request.get('delete_key'))
        
        project_key=key.get()
        user_info = self.auth.get_user_by_session()
        project_key.modified_by = user_info['email_address']
        project_key.modified_date = datetime.now()
        project_key.status = False
        project_key.put()
        
        projmem = project.ProjectMembers().get_all(key)
        
        for mem in projmem:
            mem.modified_by = user_info['email_address']
            mem.modified_date = datetime.now()
            mem.status = False
            mem.put()
        #user_key.delete()  
        self.response.write("true")     
              
        
class DeleteProjectMember(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        projmemid = self.request.get("id")
        user_info = self.auth.get_user_by_session()
        key= ndb.Key('ProjectMembers',int(projmemid))
        projmem = key.get()
        
       # logging.info(projmem)
        
        projmem.modified_by = user_info['email_address']
        projmem.modified_date = datetime.now()
        projmem.status = False
        projmem.put()
        
        sprints = sprint.Sprint().get_by_project(projmem.projectid)
        
        project_key=self.session['current_project']  
        logging.info(project_key)
        
        user_id=user_info['user_id']
        user_key=ndb.Key('OurUser',int(user_id))
        logging.info(user_key)
        
        
        
         #for user tasks
        task_data=model.task.Task().query(model.task.Task.assignee == projmem.userid,ndb.AND(model.task.Task.status == True),ndb.AND(model.task.Task.project == project_key)).fetch()
        #logging.info(task_data)
      
        #for userstory
        userstory_data=model.product_backlog.ProductUserStory().query(model.product_backlog.ProductUserStory.assignee == projmem.userid,ndb.AND(model.product_backlog.ProductUserStory.status == True,ndb.AND(model.product_backlog.ProductUserStory.project_key == project_key))).fetch()
       # logging.info(userstory_data)
        
       # logging.info(projmodel)
        
        task_list=[]
        userstory_list=[]
        
        
        
        for tasks in task_data:
                tasks_key=tasks.key.get()
                tasks_key.assignee = user_key
              #  tasks_key.put()
                task_list.append(tasks_key)
                logging.info(tasks_key)
            
        logging.info(task_list)
        ndb.put_multi(task_list)
            
                
        for userstories in userstory_data:
                userstories_key=userstories.key.get()
                userstories_key.assignee = user_key
             #   userstories_key.put()
                userstory_list.append(userstories_key)
                logging.info(userstories_key)
            
        ndb.put_multi(userstory_list)   
            
        logging.info(userstory_list)
    
        if not sprints:
            logging.info("No sprints")
        else:
            task = taskqueue.add(
            queue_name = "my-push-queue",                 
            url='/deleteusereffortspersist',
            params={'projectid': projmem.projectid.id(),'userid':projmem.userid.id()})
        
        
     #   projmem.status = 'False'
     #   projmem.set()
        #projmem.delete_entity(projmemid)
        self.response.write("success")
        
class DeleteEstimates(BaseHandler):
    @checkdomain
    def post(self,*args,**kargs):
        logging.info("it is here "+self.request.__str__())
        estimatesid = self.request.get("id")
        key= ndb.Key('Estimation',int(estimatesid))
        est_info = key.get()
        user_info = self.auth.get_user_by_session()
        est_info.modified_by = user_info['email_address']
        est_info.modified_date = datetime.now()
        est_info.status = False
        est_info.put()
        
        #esti = project.Estimation()
        
       # esti.status = 'False'
       # esti.set()
        
        #esti.delete_entity(estimatesid)
        self.response.write("success")
        
class ViewProject(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
        currentUser=self.auth.get_user_by_session()
        logging.info("it is here proj "+self.request.get("proj_id"))
        projkey = int(self.request.get("proj_id"))
        projmodel=project.Project()
        proj=projmodel.get_proj(projkey)
        
        #proj.startDate = proj.startDate.strftime('%d/%m/%Y')
        #proj.endDate =   proj.endDate.strftime('%d/%m/%Y')
        logging.info("it is here proj "+proj.__str__())
        
        estimationmodel = project.Estimation()
        esti = estimationmodel.get_all(ndb.Key('Project',projkey))
        
        projectmembermodel = project.ProjectMembers()
        projmem = projectmembermodel.get_active(ndb.Key('Project',projkey))
        
        groupmodel = user.Groups().query(ndb.AND(user.Groups.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key,user.Groups.application_level == False,user.Groups.status == True)).fetch()
        groupmodel1 = user.Groups().query(ndb.AND(user.Groups.tenant_key==None,user.Groups.application_level == False,user.Groups.status == True)).fetch()
        groupmodel.extend(groupmodel1)
        currentUser=self.auth.get_user_by_session()
        usermodel = user.OurUser().query(ndb.AND(user.OurUser.tenant_key==self.user_model.get_by_id(currentUser['user_id']).tenant_key, user.OurUser.status == True )).fetch()
        for usr in usermodel:
            for mem in projmem:
                if(usr.key == mem.userid):
                    usermodel.remove(usr)
                    
        user_id=currentUser['user_id']
        user_key=ndb.Key('OurUser',int(user_id))
        logging.info(user_key)
        
        product_owner=project.ProjectMembers().query(project.ProjectMembers.projectid == ndb.Key('Project',projkey) , ndb.AND(project.ProjectMembers.userRole == 'Product Owner',ndb.AND(project.ProjectMembers.status == True))).get()
        
        if product_owner.userid == user_key:
            a=True
        else:
            a=False
        
        self.render_template("user_new/viewproject.html",{"project":proj,"userslist":usermodel,'estimation':esti,'projmem':projmem,'roles':groupmodel,'product_owner':a})
        
        
class GetTeamMembersForProject(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
       
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project = projectkey.get()
        
        self.render_template("viewteammembers.html",{"project":project})
        
class EditProject(BaseHandler):
    @checkdomain
    def get(self,*args,**kargs):
       
      
        projectkey = ndb.Key(urlsafe=self.request.get("key"))
        project_list = projectkey.get()
        
   
        logging.info("test")
        estimation = project.Estimation()
        esti = estimation.query(project.Estimation.projectid == projectkey ).fetch()
        
        logging.info(esti)
        
        self.render_template("editproject.html",{"project":project_list,"estimation":esti})