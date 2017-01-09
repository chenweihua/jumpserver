# coding: utf-8
import os
from models import Project,ProjectGroup,Env,Config
from jumpserver.api import get_object


def group_add_project(group, project_id=None, name=None):
    """
    用户组中添加用户
    ProjectGroup Add a project
    """
    if project_id:
        project = get_object(Project, id=project_id)
    else:
        project = get_object(Project, name=name)

    if project:
        group.project_set.add(project)

def group_update_project(group_id, project_id_list):
    """
    project group update member
    用户组更新成员
    """
    project_group = get_object(ProjectGroup, id=group_id)
    if project_group:
        project_group.project_set.clear()
        for project_id in project_id_list:
            project = get_object(ProjectGroup, id=project_id)
            if isinstance(project, ProjectGroup):
                project_group.project_set.add(project)

def db_add_project_group(**kwargs):
    """
    add a user group in database
    数据库中添加用户组
    """
    name = kwargs.get('name')
    code = kwargs.get('code')
    projectgroup = get_object(ProjectGroup, name=name)
    proejcts = kwargs.pop('groups_id')

    if not projectgroup:
        projectgroup = ProjectGroup(**kwargs).save()
        for project_id in proejcts:
            group_add_project(projectgroup, project_id)




def db_add_project(**kwargs):
    """
    add a user in database
    数据库中添加用户
    """
    groups_post = kwargs.pop('groups')
    role = kwargs.get('role', 'CU')
    projects_list=kwargs.pop(('project_list'))
    project = Project(**kwargs)
    project.save()
    if groups_post:
           group_select = []
           for group_id in groups_post:
               group = group.objects.filter(id=group_id)
               group_select.extend(group)
           project.projectgroup = group_select
    if projects_list:
          project_select =[]
          for project_id in projects_list:
              devproject=Project.objects.filter(id=project_id)
              project_select.extend(devproject)
          project.depproject =project_select

    return project


def db_update_project(**kwargs):
    """
    update a user info in database
    数据库更新用户信息
    """
    groups_post = kwargs.pop('groups')
    project_id = kwargs.pop('project_id')
    project = Project.objects.filter(id=project_id)
    if project:
        project_get = project[0]
        project.update(**kwargs)

    else:
        return None

    group_select = []
    if groups_post:
        for group_id in groups_post:
            projectgroup = ProjectGroup.objects.filter(id=group_id)
            group_select.extend(projectgroup)
    project_get.group = group_select

def db_del_project(name):
    """
    delete a user from database
    从数据库中删除用户
    """
    project = get_object(Project, name=name)
    if project:
        project.delete()



def get_file_context(project_id,env_id,file):
    if project_id and env_id:
        try:
            project = Project.objects.filter(id=project_id)
            config=Config.objects.all().fileter(project=project,file=file)

            env=Env.objects.all().filter(id=env_id)
            if config.path is None:
                file=project.work+'/'+project.web_work+'src/resource'+file
            else:
                file=project.work+'/'+project.web_work+'src/resource'+'/'+config.path+'/'+file
            f= open(file,'rb')
            f.close
            return f.read()
        except:
            f.close()

def write_file_context(project_id,env_id,file,context):
    if project_id and env_id:
        try:
            project=Project.objects.all().filter(id=project_id,file=file)
            config=Config.objects.all().fileter(project=project,file=file)
            env=Env.objects.all().filter(id=env_id)
            if config.path is None:
                if  os.path.exists(env.rsync_resouce+'/'+env.code+'/'+project.code+'/'+'ROOT/classes'+'/'+config.path):
                    pass
                else:
                    os.makedirs(env.rsync_resouce+'/'+env.code+'/'+project.code+'/'+'ROOT/classes'+'/'+config.path)
                file=env.rsync_resouce+'/'+env.code+'/'+'/'+project.code+'/'+'ROOT/classes'+'/'+config.path+'/'+file
            else:
                if  os.path.exists(env.rsync_resouce+'/'+env.code+'/'+project.code+'/'+'ROOT/classes'):
                    pass
                else:
                    os.makedirs(env.rsync_resouce+'/'+env.code+'/'+project.code+'/'+'ROOT/classes')
                file=env.rsync_resouce+'/'+env.code+'/'+'/'+project.code+'/'+'ROOT/classes'+'/'+config.path+'/'+file
            file=env.rsync_resouce+'/'+env.code+'/'+'/'+project.code+'/'+'ROOT/classes'+'/'+file

            f= open(file,'wb')
            f.write(context)
            f.close()
        except:
            f.close()
