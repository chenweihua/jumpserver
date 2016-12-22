# coding: utf-8

from models import Project,ProjectDefaultConfig,ProjectConfig,ProjectGroup,PublishProject
from jumpserver.api import get_object

def group_add_project(group, project_id=None, project_name=None):
    """
    用户组中添加用户
    ProjectGroup Add a project
    """
    if project_id:
        project = get_object(Project, id=project_id)
    else:
        project = get_object(Project, username=project_name)

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
    group_name = kwargs.get('group_name')
    group_code = kwargs.get('group_code')
    sort = kwargs.get('sort')
    projectgroup = get_object(ProjectGroup, project_name=group_name)
    proejcts = kwargs.pop('project_id')

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
    proejct = Project(**kwargs)
    proejct.save()
    if groups_post:
        group_select = []
        for group_id in groups_post:
            group = ProjectGroup.objects.filter(id=group_id)
            group_select.extend(group)
        proejct.projectgroup = group_select
    return proejct


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
            group = ProjectGroup.objects.filter(id=group_id)
            group_select.extend(group)
    project_get.projectgroup = group_select

def db_del_project(project_name):
    """
    delete a user from database
    从数据库中删除用户
    """
    project = get_object(Project, project_name=project_name)
    if project:
        project.delete()





