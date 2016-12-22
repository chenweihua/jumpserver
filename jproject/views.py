# coding: utf-8
# Author: Guanghongwei
# Email: ibuler@qq.com


from django.shortcuts import get_object_or_404
from django.db.models import Q
from jproject.project_api import *
from jumpserver.api import require_role,ServerError,my_render,pages
from jperm.perm_api import get_group_user_perm
from jproject.models import  Project, PublishProject,ProjectGroup
from juser.models import  User
from django.http import HttpResponse, Http404,HttpResponseRedirect
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
        sort =  request.POST.get('sort','')
        Project_selected=request.POST.get('Project_selected','')


        try:
            if not group_name:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not group_code:
                error = u'组名 不能为空'
                raise ServerError(error)
            db_add_project(group_name=group_name, groups_id=Project_selected,group_code=group_code,sort=sort)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % group_name

    return my_render('jproject/projectgroup_add.html', locals(), request)

@require_role(role='user')
def project_group_list(request):
    """
    list project group
    项目组列表
    """
    header_title, path1, path2 = '查看项目组', '项目管理', '查看项目组'
    keyword = request.GET.get('search', '')
    proejct_group_list = ProjectGroup.objects.all().order_by('name')
    group_id = request.GET.get('id', '')

    if keyword:
        proejct_group_list = proejct_group_list.filter(Q(project_name__icontains=keyword))

    if group_id:
        proejct_group_list = proejct_group_list.filter(id=int(group_id))

    proejct_group_list, p, project_groups, page_range, current_page, show_first, show_end = pages(proejct_group_list, request)
    return my_render('juser/projectgroup_list.html', locals(), request)

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

    return my_render('jproject/projectgroup_edit.html', locals(), request)


@require_role(role='user')
def project_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加项目组', '项目管理', '添加项目组'
    project_all = Project.objects.all()

    if request.method == 'POST':
        project_name = request.POST.get('project_name', '')
        project_code =  request.POST.get('project_code','')
        scm_address =  request.POST.get('scm_address','')
        scm_url =  request.POST.get('scm_url','')
        scm_model_type =  request.POST.get('scm_model_type','')
        scm_branch =  request.POST.get('scm_branch','')
        user_id =  request.POST.get('user_id','')
        proejct_username =  request.POST.get('proejct_username','')
        project_phone =  request.POST.get('project_phone','')
        project_work =  request.POST.get('project_work','')
        project_web_work =  request.POST.get('project_web_work','')
        comment = request.POST.get('comment', '')

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

            db_add_project(name=project_name, users_id=users_selected, comment=comment)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % group_name

    return my_render('juser/project_add.html', locals(), request)

@require_role(role='user')
def project_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看项目组', '项目管理', '查看项目组'
    keyword = request.GET.get('search', '')
    user_group_list = UserGroup.objects.all().order_by('name')
    group_id = request.GET.get('id', '')

    if keyword:
        user_group_list = user_group_list.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))

    if group_id:
        user_group_list = user_group_list.filter(id=int(group_id))

    user_group_list, p, user_groups, page_range, current_page, show_first, show_end = pages(user_group_list, request)
    return my_render('juser/group_list.html', locals(), request)


@require_role(role='user')
def project_del(request):
    """
    del a group
    删除项目组
    """
    group_ids = request.GET.get('id', '')
    group_id_list = group_ids.split(',')
    for group_id in group_id_list:
        UserGroup.objects.filter(id=group_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def project_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目组', '项目管理', '编辑项目组'

    if request.method == 'GET':
        group_id = request.GET.get('id', '')
        user_group = get_object(UserGroup, id=group_id)
        # user_group = UserGroup.objects.get(id=group_id)
        users_selected = User.objects.filter(group=user_group)
        users_remain = User.objects.filter(~Q(group=user_group))
        users_all = User.objects.all()

    elif request.method == 'POST':
        group_id = request.POST.get('group_id', '')
        group_name = request.POST.get('group_name', '')
        comment = request.POST.get('comment', '')
        users_selected = request.POST.getlist('users_selected')

        try:
            if '' in [group_id, group_name]:
                raise ServerError('组名不能为空')

            if len(UserGroup.objects.filter(name=group_name)) > 1:
                raise ServerError(u'%s 项目组已存在' % group_name)
            # add user group
            user_group = get_object_or_404(UserGroup, id=group_id)
            user_group.user_set.clear()

            for user in User.objects.filter(id__in=users_selected):
                user.group.add(UserGroup.objects.get(id=group_id))

            user_group.name = group_name
            user_group.comment = comment
            user_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('user_group_list'))
        else:
            users_all = User.objects.all()
            users_selected = User.objects.filter(group=user_group)
            users_remain = User.objects.filter(~Q(group=user_group))

    return my_render('juser/group_edit.html', locals(), request)



@require_role(role='super')
def proejctconfig_add(request):
    header_title, path1, path2 = '编辑项目', '项目管理', '编辑项目'
    if request.method == 'GET':
        user_id = request.GET.get('id', '')
        if not user_id:
            return HttpResponseRedirect(reverse('index'))

        user_role = {'SU': u'超级管理员', 'CU': u'普通项目'}
        user = get_object(User, id=user_id)
        group_all = UserGroup.objects.all()
        if user:
            groups_str = ' '.join([str(group.id) for group in user.group.all()])
            admin_groups_str = ' '.join([str(admin_group.group.id) for admin_group in user.admingroup_set.all()])

    else:
        user_id = request.GET.get('id', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        groups = request.POST.getlist('groups', [])
        role_post = request.POST.get('role', 'CU')
        admin_groups = request.POST.getlist('admin_groups', [])
        extra = request.POST.getlist('extra', [])
        is_active = True if '0' in extra else False
        email_need = True if '1' in extra else False
        user_role = {'SU': u'超级管理员', 'GA': u'部门管理员', 'CU': u'普通项目'}

        if user_id:
            user = get_object(User, id=user_id)
        else:
            return HttpResponseRedirect(reverse('user_list'))

        db_update_user(user_id=user_id,
                       password=password,
                       name=name,
                       email=email,
                       groups=groups,
                       admin_groups=admin_groups,
                       role=role_post,
                       is_active=is_active)

        if email_need:
            msg = u"""
            Hi %s:
                您的信息已修改，请登录跳板机查看详细信息
                地址：%s
                项目名： %s
                密码：%s (如果密码为None代表密码为原密码)
                权限：：%s

            """ % (user.name, URL, user.username, password, user_role.get(role_post, u''))
            send_mail('您的信息已修改', msg, MAIL_FROM, [email], fail_silently=False)

        return HttpResponseRedirect(reverse('user_list'))
    return my_render('juser/user_edit.html', locals(), request)



@require_role(role='super')
def proejctconfig_edit(request):
    header_title, path1, path2 = '编辑项目', '项目管理', '编辑项目'
    if request.method == 'GET':
        user_id = request.GET.get('id', '')
        if not user_id:
            return HttpResponseRedirect(reverse('index'))

        user_role = {'SU': u'超级管理员', 'CU': u'普通项目'}
        user = get_object(User, id=user_id)
        group_all = UserGroup.objects.all()
        if user:
            groups_str = ' '.join([str(group.id) for group in user.group.all()])
            admin_groups_str = ' '.join([str(admin_group.group.id) for admin_group in user.admingroup_set.all()])

    else:
        user_id = request.GET.get('id', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        groups = request.POST.getlist('groups', [])
        role_post = request.POST.get('role', 'CU')
        admin_groups = request.POST.getlist('admin_groups', [])
        extra = request.POST.getlist('extra', [])
        is_active = True if '0' in extra else False
        email_need = True if '1' in extra else False
        user_role = {'SU': u'超级管理员', 'GA': u'部门管理员', 'CU': u'普通项目'}

        if user_id:
            user = get_object(User, id=user_id)
        else:
            return HttpResponseRedirect(reverse('user_list'))

        db_update_user(user_id=user_id,
                       password=password,
                       name=name,
                       email=email,
                       groups=groups,
                       admin_groups=admin_groups,
                       role=role_post,
                       is_active=is_active)

        if email_need:
            msg = u"""
            Hi %s:
                您的信息已修改，请登录跳板机查看详细信息
                地址：%s
                项目名： %s
                密码：%s (如果密码为None代表密码为原密码)
                权限：：%s

            """ % (user.name, URL, user.username, password, user_role.get(role_post, u''))
            send_mail('您的信息已修改', msg, MAIL_FROM, [email], fail_silently=False)

        return HttpResponseRedirect(reverse('user_list'))
    return my_render('juser/user_edit.html', locals(), request)





