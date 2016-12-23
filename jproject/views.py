# coding: utf-8
# Author: Guanghongwei
# Email: ibuler@qq.com

from django.shortcuts import get_object_or_404
from django.db.models import Q
from jproject.project_api import *
from jumpserver.api import require_role,ServerError,my_render,pages
from jproject.models import  Project, ProjectGroup,PublishEnv,PublishConfig,PublishProject
from juser.models import  User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

@require_role(role='user')
def project_group_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加项目组', '项目管理', '添加项目组'
    project_all = Project.objects.all()

    if request.method == 'POST':
        group_code = request.POST.get('group_code', '')
        group_name =  request.POST.get('group_name','')
        projects_selected=request.POST.get('projects_selected','')
        try:
            if not group_name:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not group_code:
                error = u'组名 不能为空'
                raise ServerError(error)
            db_add_project_group(group_name=group_name, groups_id=projects_selected,group_code=group_code)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % group_name

    return my_render('jproject/group_add.html', locals(), request)

@require_role(role='user')
def project_group_list(request):
    """
    list project group
    项目组列表
    """
    header_title, path1, path2 = '查看项目组', '项目管理', '查看项目组'
    keyword = request.GET.get('search', '')
    proejct_group_list = ProjectGroup.objects.all().order_by('group_name')
    group_id = request.GET.get('id', '')

    if keyword:
        proejct_group_list = proejct_group_list.filter(Q(group_name__icontains=keyword)|Q(group_code__icontains=keyword))

    if group_id:
        proejct_group_list = proejct_group_list.filter(id=int(group_id))

    proejct_group_list, p, project_groups, page_range, current_page, show_first, show_end = pages(proejct_group_list, request)
    return my_render('jproject/group_list.html', locals(), request)

@require_role(role='user')
def project_group_del(request):
    """
    del a project group
    删除项目组
    """
    group_ids = request.GET.get('id', '')
    group_id_list = group_ids.split(',')
    for group_id in group_id_list:
        ProjectGroup.objects.filter(id=group_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def project_group_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目组', '项目管理', '编辑项目组'

    if request.method == 'GET':
        group_id = request.GET.get('id', '')
        project_group = get_object(ProjectGroup, id=group_id)
        # user_group = UserGroup.objects.get(id=group_id)
        Project_selected = Project.objects.filter(group=project_group)
        Project_remain = Project.objects.filter(~Q(group=project_group))
        Project_all = Project.objects.all()

    elif request.method == 'POST':
        group_id = request.POST.get('group_id', '')
        group_name = request.POST.get('group_name', '')
        sort = request.POST.get('sort', '')
        group_code = request.POST.get('group_code', '')
        Project_selected = request.POST.getlist('Project_selected')

        try:
            if '' in [group_id, group_name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=group_name)) > 1:
                raise ServerError(u'%s 项目组已存在' % group_name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=group_id)
            project_group.project_set.clear()

            for project in Project.objects.filter(id__in=Project_selected):
                project.group.add(ProjectGroup.objects.get(id=group_id))

            project_group.group_name = group_name
            project_group.sort = sort
            project_group.group_code=group_code
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('user_group_list'))
        else:
            Project_all = Project.objects.all()
            Project_selected = Project.objects.filter(group=project_group)
            Project_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('jproject/group_edit.html', locals(), request)


@require_role(role='user')
def project_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加项目组', '项目管理', '添加项目组'
    group_all = ProjectGroup.objects.all()
    project_all=Project.objects.all()



    if request.method == 'POST':
        project_name = request.POST.get('project_name', '')
        project_code =  request.POST.get('project_code','')
        scm_address =  request.POST.get('scm_address','')
        scm_url =  request.POST.get('scm_url','')
        scm_model_type =  request.POST.get('scm_model_type','')
        scm_branch =  request.POST.get('scm_branch','')
        user_id = request.GET.get('id', '')
        proejct_username =  request.POST.get('proejct_username','')
        project_phone =  request.POST.get('project_phone','')
        project_work =  request.POST.get('project_work','')
        project_web_work =  request.POST.get('project_web_work','')
        comment = request.POST.get('comment', '')
        groups_post=request.POST.get('groups_list','')
        projects_list=request.POST.get('projects_list','')


        try:
            if not project_name:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not project_code:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not scm_url:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not project_work:
                error = u'组名 不能为空'
                raise ServerError(error)

            db_add_project(name=project_name, groups=groups_post, project_code=project_code,scm_address=scm_address,scm_url=scm_url,scm_model_type=scm_model_type,
                           scm_branch=scm_branch,user_id=user_id,proejct_username=proejct_username,project_phone=project_phone,project_work=project_work,
                           project_web_work=project_web_work,comment=comment,project_list=projects_list)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % project_name

    return my_render('jproject/project_add.html', locals(), request)

@require_role(role='user')
def project_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看项目', '项目管理', '查看项目'
    keyword = request.GET.get('search', '')
    gid = request.GET.get('gid', '')
    projects_list = Project.objects.all().order_by('project_name')

    if gid:
        project_group = ProjectGroup.objects.filter(id=int(gid))
        if project_group:
            project_group=project_group[0]
            projects_list=project_group.project_set.all()

    if keyword:
        projects_list = projects_list.filter(Q(project_name__icontains=keyword) | Q(project_code__icontains=keyword))


    projects_list, p, projects, page_range, current_page, show_first, show_end = pages(projects_list, request)
    return my_render('jproject/project_list.html', locals(), request)


@require_role(role='user')
def project_del(request):
    """
    del a group
    删除项目组
    """
    group_ids = request.GET.get('id', '')
    group_id_list = group_ids.split(',')
    for group_id in group_id_list:
        ProjectGroup.objects.filter(id=group_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def project_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目组', '项目管理', '编辑项目组'

    if request.method == 'GET':
        group_id = request.GET.get('id', '')
        project_group = get_object(ProjectGroup, id=group_id)
        # user_group = UserGroup.objects.get(id=group_id)
        projects_selected = User.objects.filter(projectgroup=project_group)
        projects_remain = User.objects.filter(~Q(projectgroup=project_group))
        projects_all = User.objects.all()

    elif request.method == 'POST':
        group_id = request.POST.get('group_id', '')
        group_name = request.POST.get('group_name', '')
        comment = request.POST.get('comment', '')
        projects_selected = request.POST.getlist('projects_selected')

        try:
            if '' in [group_id, group_name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=group_name)) > 1:
                raise ServerError(u'%s 项目组已存在' % group_name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=group_id)
            project_group.user_set.clear()

            for project in Project.objects.filter(id__in=projects_selected):
                project.projectgroup.add(ProjectGroup.objects.get(id=group_id))

            project_group.name = group_name
            project_group.comment = comment
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('project_group_list'))
        else:
            projects_all = Project.objects.all()
            projects_selected = Project.objects.filter(group=project_group)
            projects_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('jproject/project_edit.html', locals(), request)







@require_role(role='user')
def project_env_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '发布环境', '发布管理', '添加项发布'
    group_all = PublishEnv.objects.all()
    project_all=Project.objects.all()



    if request.method == 'POST':


        try:
            if not project_name:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not project_code:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not scm_url:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not project_work:
                error = u'组名 不能为空'
                raise ServerError(error)

            db_add_project(name=project_name, groups=groups_post, project_code=project_code,scm_address=scm_address,scm_url=scm_url,scm_model_type=scm_model_type,
                           scm_branch=scm_branch,user_id=user_id,proejct_username=proejct_username,project_phone=project_phone,project_work=project_work,
                           project_web_work=project_web_work,comment=comment,project_list=projects_list)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % project_name

    return my_render('juser/env_add.html', locals(), request)

@require_role(role='user')
def project_env_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看项目组', '项目管理', '查看项目组'
    keyword = request.GET.get('search', '')
    env_list = PublishEnv.objects.all().order_by('config_name')
    group_id = request.GET.get('id', '')

    if keyword:
        user_group_list = user_group_list.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))

    if group_id:
        user_group_list = user_group_list.filter(id=int(group_id))

    user_group_list, p, user_groups, page_range, current_page, show_first, show_end = pages(user_group_list, request)
    return my_render('juser/env_list.html', locals(), request)


@require_role(role='user')
def project_env_del(request):
    """
    del a group
    删除项目组
    """
    group_ids = request.GET.get('id', '')
    group_id_list = group_ids.split(',')
    for group_id in group_id_list:
        ProjectGroup.objects.filter(id=group_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def project_env_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目组', '项目管理', '编辑项目组'

    if request.method == 'GET':
        group_id = request.GET.get('id', '')
        project_group = get_object(ProjectGroup, id=group_id)
        # user_group = UserGroup.objects.get(id=group_id)
        projects_selected = User.objects.filter(projectgroup=project_group)
        projects_remain = User.objects.filter(~Q(projectgroup=project_group))
        projects_all = User.objects.all()

    elif request.method == 'POST':
        group_id = request.POST.get('group_id', '')
        group_name = request.POST.get('group_name', '')
        comment = request.POST.get('comment', '')
        projects_selected = request.POST.getlist('projects_selected')

        try:
            if '' in [group_id, group_name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=group_name)) > 1:
                raise ServerError(u'%s 项目组已存在' % group_name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=group_id)
            project_group.user_set.clear()

            for project in Project.objects.filter(id__in=projects_selected):
                project.projectgroup.add(ProjectGroup.objects.get(id=group_id))

            project_group.name = group_name
            project_group.comment = comment
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('project_group_list'))
        else:
            projects_all = Project.objects.all()
            projects_selected = Project.objects.filter(group=project_group)
            projects_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('juser/env_edit.html', locals(), request)













