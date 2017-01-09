# coding: utf-8
# Author: Guanghongwei
# Email: ibuler@qq.com
# from django.db import connection
from django.shortcuts import get_object_or_404
from django.db.models import Q
from jproject.project_api import *
from jproject.api_publish import *
from jumpserver.api import require_role,ServerError,my_render,pages
from jproject.models import  Project,ProjectGroup,PublishConfig,Publish,SCMToken,SCMSetting
from juser.models import  User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from jproject.forms import *
from jproject.gitlab import  Gitlab
import json
from jproject.forms import *
from django.shortcuts import render
# from django.http import JsonResponse

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
        code = request.POST.get('code', '')
        name =  request.POST.get('name','')
        projects_selected=request.POST.get('projects_selected','')
        try:
            if not name:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not code:
                error = u'组名 不能为空'
                raise ServerError(error)
            db_add_project_group(name=name, groups_id=projects_selected,code=code)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % name

    return my_render('jproject/group_add.html', locals(), request)

@require_role(role='user')
def project_group_list(request):
    """
    list project group
    项目组列表
    """
    header_title, path1, path2 = '查看项目组', '项目管理', '查看项目组'
    keyword = request.GET.get('search', '')
    group_list = ProjectGroup.objects.all().order_by('name')
    id = request.GET.get('id', '')

    if keyword:
        group_list = group_list.filter(Q(name__icontains=keyword)|Q(code__icontains=keyword))

    if id:
        group_list = group_list.filter(id=int(id))

    group_list, p, groups, page_range, current_page, show_first, show_end = pages(group_list, request)
    return my_render('jproject/group_list.html', locals(), request)

@require_role(role='user')
def project_group_del(request):
    """
    del a project group
    删除项目组
    """
    ids = request.GET.get('id', '')
    id_list = ids.split(',')
    for id in id_list:
        ProjectGroup.objects.filter(id=id).delete()

    return HttpResponse('删除成功')

@require_role(role='user')
def getProject(request):
    """
    del a project group
    删除项目组
    """
    id = request.GET.get('id', '')
    scmsetting = SCMSetting.objects.get(id=id)
    gitlab_project_list=[]
    if scmsetting:
        gitlab =Gitlab(scmsetting.scm_url,rootoken=scmsetting.default_token)
    else:
        return HttpResponse(json.dumps(gitlab_project_list))
    for project in gitlab.get_projects():
        gitlab_project_list.append(project)

    return HttpResponse(json.dumps(gitlab_project_list),content_type="application/json")

    # ufs = serializers.serialize("json", UploadFile.objects.all().order_by('-pub_date'))
    # return HttpResponse(ufs, content_type="application/json")



@require_role(role='user')
def project_group_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目组', '项目管理', '编辑项目组'

    if request.method == 'GET':
        id = request.GET.get('id', '')
        group = get_object(ProjectGroup, id=id)
        project_selected = Project.objects.filter(group=group)
        project_remain = Project.objects.filter(~Q(group=group))
        project_all = Project.objects.all()

    elif request.method == 'POST':
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        sort = request.POST.get('sort', '')
        code = request.POST.get('code', '')
        project_selected = request.POST.getlist('project_selected')

        try:
            if '' in [id, name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=name)) > 1:
                raise ServerError(u'%s 项目组已存在' % name)
            # add user group
            group = get_object_or_404(ProjectGroup, id=id)
            group.project_set.clear()

            for project in Project.objects.filter(id__in=project_selected):
                project.group.add(ProjectGroup.objects.get(id=id))

            group.name = name
            group.sort = sort
            group.code=code
            group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('user_list'))
        else:
            project_all = Project.objects.all()
            project_selected = Project.objects.filter(group=group)
            project_remain = Project.objects.filter(~Q(group=group))

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
    # if request.user.is_superuser:
    #     scmsettings = SCMSetting.objects.all()
    # else:
    #
    #     scmtokens = SCMToken.objects.filter(fullname=request.user)
    #     scmsettings = scmtokens.scmsetting_set.all()
    #     if scmsettings is None:
    #         scmsettings = SCMSetting.objects.all()
    scm=request.GET.get('scm','')
    scm_project_selected = []
    if scm is None:
        scm_project_selected.append(('id','-----'),)
    else:
        try:
            scmsetting=SCMSetting.objects.all().filter(id=int(scm))
            host = scmsetting.hostname
            rootoken = scmsetting.rootoken
            gitlab = Gitlab(host, rootoken)
            gitlab_list= gitlab.get_all_projects()
            scm_project_selected.append(('id','-----'),)
            for scm_project in gitlab_list:
                scm_project_selected.append((scm_project['pro_id'],scm_project['pro_url']),)
        except:
            scm_project_selected.append(('id','-----'),)
    pf = ProjectForm(scm_project_selected)
    if request.method == 'POST':
        form_post = ProjectForm(request.POST)
        name = request.POST.get('name', '')
        code =  request.POST.get('code','')
        scm_url =  request.POST.get('scm_url','')
        scm_model_type =  request.POST.get('scm_model_type','')
        scm_type =  request.POST.get('scm_type','')
        manage =  request.POST.get('project_phone','')
        phone =  request.POST.get('project_phone','')
        work =  request.POST.get('project_work','')
        web_work =  request.POST.get('project_web_work','')
        backup =  request.POST.get('project_web_work','')
        try:
            if not name:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not code:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not scm_url:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not work:
                error = u'组名 不能为空'
                raise ServerError(error)

            if Project.objects.filter(name=unicode(name)):
                error = u'该主机名 %s 已存在!' % name
                raise ServerError(error)
            if len(name) > 54:
                error = u"主机名长度不能超过53位!"
                raise ServerError(error)
        except ServerError:
            pass
        else:
            if form_post.is_valid():
                project_save = form_post.save(commit=False)
                form_post.save()
                form_post.save_m2m()

                msg = u'项目 %s 添加成功' % name
            else:
                esg = u'项目 %s 添加失败' % name

    return my_render('jproject/project_add.html', locals(), request)

    # return render(request,'jproject/project_add.html', locals(), content_type='application/xhtml+xml')

@require_role(role='user')
def project_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看项目', '项目管理', '查看项目'
    keyword = request.GET.get('search', '')
    gid = request.GET.get('gid', '')
    projects_list = Project.objects.all().order_by('name')

    if gid:
        project_group = ProjectGroup.objects.filter(id=int(gid))
        if project_group:
            project_group=project_group[0]
            projects_list=project_group.project_set.all()

    if keyword:
        projects_list = projects_list.filter(Q(name__icontains=keyword) | Q(code__icontains=keyword))


    projects_list, p, projects, page_range, current_page, show_first, show_end = pages(projects_list, request)
    return my_render('jproject/project_list.html', locals(), request)


@require_role(role='user')
def project_del(request):
    """
    del a group
    删除项目组
    """
    ids = request.GET.get('id', '')
    id_list = ids.split(',')
    for id in id_list:
        ProjectGroup.objects.filter(id=id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def project_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑项目组', '项目管理', '编辑项目组'

    if request.method == 'GET':
        id = request.GET.get('id', '')
        project_group = get_object(ProjectGroup, id=id)
        # user_group = UserGroup.objects.get(id=id)
        projects_selected = User.objects.filter(group=project_group)
        projects_remain = User.objects.filter(~Q(group=project_group))
        projects_all = User.objects.all()

    elif request.method == 'POST':
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')
        projects_selected = request.POST.getlist('projects_selected')

        try:
            if '' in [id, name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=name)) > 1:
                raise ServerError(u'%s 项目组已存在' % name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=id)
            project_group.user_set.clear()

            for project in Project.objects.filter(id__in=projects_selected):
                project.projectgroup.add(ProjectGroup.objects.get(id=id))

            project_group.name = name
            project_group.comment = comment
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('project_list'))
        else:
            projects_all = Project.objects.all()
            projects_selected = Project.objects.filter(group=project_group)
            projects_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('jproject/project_edit.html', locals(), request)


@require_role(role='user')
def config_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '发布环境', '发布管理', '添加发布环境'
    ef=EnvForm()
    if request.method == 'POST':
        ef_post=EnvForm(request.POST)
        name=request.POST.get("name",'')
        code=request.POST.get("code",'')
        procode=request.POST.get("precode",'')
        try:
            if not name:
                error = u'发布环境 不能为空'
                raise ServerError(error)
            if not code:
                error = u'发布环境 不能为空'
                raise ServerError(error)

        except ServerError:
            pass
        except TypeError:
            error = u'添加环境失败'
        else:
            if ef_post.is_valid():
                af_save = ef_post.save(commit=True)
                msg = u'添加环境 %s 成功' % name
            else:
                error = u'添加环境失败'

    return my_render('jproject/env_add.html', locals(), request)

@require_role(role='user')
def config_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看发布环境', '发布环境', '发布环境'
    keyword = request.GET.get('search', '')
    env_list = Env.objects.all().order_by('name')
    env_id = request.GET.get('id', '')

    if keyword:
        env_list = env_list.filter(Q(name__icontains=keyword) | Q(code__icontains=keyword))

    if env_id:
        env_list = env_list.filter(id=int(env_id))

    env_list, p, envs, page_range, current_page, show_first, show_end = pages(env_list, request)
    return my_render('jproject/env_list.html', locals(), request)


@require_role(role='user')
def config_del(request):
    """
    del a group
    删除项目组
    """
    env_ids = request.GET.get('id', '')
    end_id_list = env_ids.split(',')
    for env_id in end_id_list:
        Env.objects.filter(id=env_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def config_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑发布环境', '发布环境', '编辑发布环境'

    env_id=request.GET.get('envid','')
    projects_all = Project.objects.all()

    if request.method == 'GET':

        publisenv = get_object(Env, id=env_id)
        # user_group = UserGroup.objects.get(id=id)
        projects_selected = PublishConfig.objects.filter(env=publisenv)
        projects_remain = PublishConfig.objects.filter(~Q(env=publisenv))
    elif request.method == 'POST':
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')
        projects_selected = request.POST.getlist('projects_selected')

        try:
            if '' in [id, name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=name)) > 1:
                raise ServerError(u'%s 项目组已存在' % name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=id)
            project_group.user_set.clear()

            for project in Project.objects.filter(id__in=projects_selected):
                project.projectgroup.add(ProjectGroup.objects.get(id=id))

            project_group.name = name
            project_group.comment = comment
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('project_list'))
        else:
            projects_all = Project.objects.all()
            projects_selected = Project.objects.filter(group=project_group)
            projects_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('jproject/env_edit.html', locals(), request)


@require_role(role='user')
def project_config_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加发布配置', '发布管理', '添加发布配置'


    cf = ConfigForm()
    if request.method == 'POST':
        form_post = ConfigForm(request.POST)
        project = request.POST.get('project', '')
        file =  request.POST.getlist('file','')
        item =  request.POST.getlist('item','')
        defaultvalue =  request.POST.getlist('defaultvalue','')
        filetype =  request.POST.getlist('filetype','')
        try:
            if not project:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not file:
                error = u'组名 不能为空'
                raise ServerError(error)


        except ServerError:
            pass
        else:
            if form_post.is_valid():
                project_save = form_post.save(commit=False)
                form_post.save()
                form_post.save_m2m()

                msg = u'项目 %s 添加成功' % item
            else:
                esg = u'项目 %s 添加失败' % item

    return my_render('jproject/config_add.html', locals(), request)



@require_role(role='user')
def project_config_edit(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加发布配置', '发布管理', '添加发布配置'

    cf = ConfigForm()
    if request.method == 'POST':
        form_post = ConfigForm(request.POST)
        project = request.POST.get('project', '')
        path =  request.POST.get('path','')
        file =  request.POST.get('file','')
        md5 =  request.POST.get('md5','')
        item =  request.POST.get('item','')
        defaultvalue =  request.POST.get('defaultvalue','')
        try:
            if not project:
                error = u'组名 不能为空'
                raise ServerError(error)
            if not file:
                error = u'组名 不能为空'
                raise ServerError(error)

        except ServerError:
            pass
        else:
            if form_post.is_valid():
                config_save = form_post.save(commit=False)
                config_save.save()
                form_post.save_m2m()

                msg = u'配置项 %s 添加成功' % item
            else:
                esg = u'配置项 %s 添加失败' % item


    return my_render('jproject/config_edit.html', locals(), request)


@require_role(role='user')
def project_config_list(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加项目配置', '项目管理', '添加项目配置'

    project_id= request.GET.get('project','')
    project_file = request.GET.get('project_file','')
    project_item = request.GET.get('item','')
    configs_list = Config.objects.all()
    if project_id:
        project=Project.objects.get(id=int(project_id))
        configs_list = configs_list.filter(project__contains=project)
    if project_file:
        configs_list  =configs_list.filter(file__contains=project_file)
    if project_item:
        configs_list  =configs_list.filter(item__contains=project_item)
    configs_list, p, configs, page_range, current_page, show_first, show_end = pages(configs_list, request)
    return my_render('jproject/config_list.html', locals(), request)

@require_role('user')
def project_config_del(request):
    """
    del a asset
    删除主机
    """
    config_id = request.GET.get('ids', '')
    config_ids = config_id.split(',')
    project = request.GET.get('project','')

    if project:
        project=Project.objects.get(id=project)
        config = get_object(Config,project=project)
        config.delete()
    for id in config_ids:
        config =get_object(Config,id=id)
        config.delete()

    return HttpResponse(u'删除成功')



@require_role(role='user')
def env_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '发布环境', '发布管理', '添加环境配置'


    if request.method == 'POST':
        project=request.POST.get("project",'')
        env=request.POST.get("env",'')
        files_list=request.POST.getList("file",'')
        items_list=request.POST.getList("item",'')
        configvalues_list=request.POST.getList("confvalue",'')
        try:
            if not project:
                error = u'发布环境 不能为空'
                raise ServerError(error)
            if not env:
                error = u'发布环境 不能为空'
                raise ServerError(error)
            # for file in files_list:
            #     db_add_publish_env(project=project, env=env,file=file)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % project

    return my_render('jproject/env_add.html', locals(), request)

@require_role(role='user')
def env_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看发布环境', '发布环境', '发布环境'
    keyword = request.GET.get('search', '')
    env_list = Env.objects.all().order_by('name')
    env_id = request.GET.get('id', '')

    if keyword:
        env_list = env_list.filter(Q(name__icontains=keyword) | Q(code__icontains=keyword))

    if env_id:
        env_list = env_list.filter(id=int(env_id))

    env_list, p, envs, page_range, current_page, show_first, show_end = pages(env_list, request)
    return my_render('jproject/env_list.html', locals(), request)


@require_role(role='user')
def env_del(request):
    """
    del a group
    删除项目组
    """
    env_ids = request.GET.get('id', '')
    end_id_list = env_ids.split(',')
    for env_id in end_id_list:
        Env.objects.filter(id=env_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def env_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑发布环境', '发布环境', '编辑发布环境'

    env_id=request.GET.get('envid','')
    projects_all = Project.objects.all()

    if request.method == 'GET':

        publisenv = get_object(Env, id=env_id)
        # user_group = UserGroup.objects.get(id=id)
        projects_selected = PublishConfig.objects.filter(env=publisenv)
        projects_remain = PublishConfig.objects.filter(~Q(env=publisenv))
    elif request.method == 'POST':
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')
        projects_selected = request.POST.getlist('projects_selected')

        try:
            if '' in [id, name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=name)) > 1:
                raise ServerError(u'%s 项目组已存在' % name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=id)
            project_group.user_set.clear()

            for project in Project.objects.filter(id__in=projects_selected):
                project.projectgroup.add(ProjectGroup.objects.get(id=id))

            project_group.name = name
            project_group.comment = comment
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('project_list'))
        else:
            projects_all = Project.objects.all()
            projects_selected = Project.objects.filter(group=project_group)
            projects_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('jproject/env_edit.html', locals(), request)




@require_role(role='user')
def publish_config_add(request):
    """
    group add view for route
    添加项目组的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '发布环境', '发布管理', '添加发布环境'
    env_id=request.GET.get("env_id",'')
    projdct_id= request.GET("project_id",'')

    if request.method == 'POST':
        name=request.POST.get("name",'')
        code=request.POST.get("code",'')
        procode=request.POST.get("precode",'')
        try:
            if not name:
                error = u'发布环境 不能为空'
                raise ServerError(error)
            if not code:
                error = u'发布环境 不能为空'
                raise ServerError(error)
            # db_add_publish_env(name=name, code=code)
        except ServerError:
            pass
        except TypeError:
            error = u'添加小组失败'
        else:
            msg = u'添加组 %s 成功' % name

    return my_render('jproject/env_add.html', locals(), request)

@require_role(role='user')
def publish_config_list(request):
    """
    list user group
    项目组列表
    """
    header_title, path1, path2 = '查看发布环境', '发布环境', '发布环境配置'
    keyword = request.GET.get('search', '')
    env_list = PublishConfig.objects.all().order_by('env')
    env_id = request.GET.get('id', '')
    project_id= request.GET.get("project_id",'')
    if env_id:
        env=Env.objects.filter(id=env_id)
        env_list.filter(env=env)
    if project_id:
        project=Project.objects.filter(id=project_id)
        env.list.filter(project=project)
    if keyword:
        env_list = env_list.filter(Q(name__icontains=keyword) | Q(code__icontains=keyword))



    env_list, p, envs, page_range, current_page, show_first, show_end = pages(env_list, request)
    return my_render('jproject/publishconfig_list.html', locals(), request)


@require_role(role='user')
def publish_config_del(request):
    """
    del a group
    删除项目组
    """
    env_ids = request.GET.get('id', '')
    end_id_list = env_ids.split(',')
    for env_id in end_id_list:
        Env.objects.filter(id=env_id).delete()

    return HttpResponse('删除成功')


@require_role(role='user')
def publish_config_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑发布环境', '发布环境', '编辑发布环境'

    env_id=request.GET.get('envid','')
    projects_all = Project.objects.all()

    if request.method == 'GET':

        publisenv = get_object(Env, id=env_id)
        # user_group = UserGroup.objects.get(id=id)
        projects_selected = PublishConfig.objects.filter(env=publisenv)
        projects_remain = PublishConfig.objects.filter(~Q(env=publisenv))
    elif request.method == 'POST':
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')
        projects_selected = request.POST.getlist('projects_selected')

        try:
            if '' in [id, name]:
                raise ServerError('组名不能为空')

            if len(ProjectGroup.objects.filter(name=name)) > 1:
                raise ServerError(u'%s 项目组已存在' % name)
            # add user group
            project_group = get_object_or_404(ProjectGroup, id=id)
            project_group.user_set.clear()

            for project in Project.objects.filter(id__in=projects_selected):
                project.projectgroup.add(ProjectGroup.objects.get(id=id))

            project_group.name = name
            project_group.comment = comment
            project_group.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('project_list'))
        else:
            projects_all = Project.objects.all()
            projects_selected = Project.objects.filter(group=project_group)
            projects_remain = Project.objects.filter(~Q(group=project_group))

    return my_render('jproject/env_edit.html', locals(), request)