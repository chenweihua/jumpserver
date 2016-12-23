# #!/usr/bin/python
# # coding:utf-8
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.shortcuts import render_to_response
# #, RequestContext
# from django.template import  RequestContext
# from gitlab import Gitlab
# from models import SCMSetting,SCMToken
# from git import Repo, cmd, Git
# from jumpserver.api import require_role
# import os
# from datetime import datetime
#
#
# @require_role(role='user')
# def ProSetting(request, Url):
#     try:
#         cProSetting = ProjectSetting.objects.get(url=Url)
#     except Exception as e:
#         print(e)
#         form = ProSettingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('listallprojectsurl'))
#         else:
#
#             form = ProSettingForm(initial={'ngxtestconf':vhost, 'ngxdevtconf':vhost, 'url':Url})
#         kwvars = {
#             'url': Url,
#             'form': form,
#             'request': request,
#         }
#         return render_to_response('GitLab/project.setting.html', kwvars, RequestContext(request))
#     else:
#         iProSetting = ProjectSetting.objects.get(url=Url)
#         form = ProSettingForm(request.POST, instance=iProSetting)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('listallprojectsurl'))
#         else:
#             form = ProSettingForm(instance=iProSetting)
#         kwvars = {
#             'url': Url,
#             'form': form,
#             'request': request,
#         }
#         return render_to_response('GitLab/project.setting.html', kwvars, RequestContext(request))
#
#
# @login_required
# @PermissionVerify()
# def Setting(request):
#     cSetting = SCMSetting.objects.all()
#     if len(cSetting) == 0:
#         form = SCMSettingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print(cSetting.get(id=1).ngxpath)
#             return HttpResponseRedirect(reverse('SCMSettingurl'))
#         else:
#             form = SCMSettingForm(initial={'testserver':'127.0.0.1', 'devserver':'127.0.0.1', 'ngxconf':ngx})
#         kwvars = {
#             'form': form,
#             'request': request,
#         }
#         return render_to_response('GitLab/setting.add.html', kwvars, RequestContext(request))
#     else:
#         iSCMSetting = SCMSetting.objects.get(id=1)
#         form = SCMSettingForm(request.POST, instance=iSCMSetting)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('SCMSettingurl'))
#         else:
#             form = SCMSettingForm(instance=iSCMSetting)
#         kwvars = {
#             'form': form,
#             'request': request,
#         }
#         return render_to_response('GitLab/setting.add.html', kwvars, RequestContext(request))
#
#
# @login_required
# @PermissionVerify()
# def AddToken(request):
#     form = TokenForm(request.POST)
#     if form.is_valid():
#         i = SCMToken()
#         form.save(commit=False)
#         usertoken = form.cleaned_data['usertoken']
#         i.usertoken = usertoken
#         i.fullname = request.user
#         i.save()
#         return HttpResponseRedirect(reverse('listallprojectsurl'))
#     else:
#         form = TokenForm()
#     kwvars = {
#         'form': form,
#         'request': request,
#     }
#     return render_to_response('GitLab/token.add.html', kwvars, RequestContext(request))
#
#
#
# def gitlab_project_list(request):
#     error =''
#     msg = ''
#     header_title,path1,path2= '','',''
#     cuser=request.user
#     if cuser.role == 'CU':
#         scmtoken=SCMToken.objects.all().filter(fullname=cuser.id)
#
#         gitlab = Gitlab(scmtoken.gitsetting.scm_url, scmtoken.scm_user_token)
#         klist=gitlab.get_user_projects(scmtoken)
#     else:
#         scmtoken=SCMSetting.objects.all()
#
#
#     if scmtoken:
#         usertoken = scmtoken
#
#     try:
#         cSCMSetting = SCMSetting.objects.get(id=1)
#     except Exception as e:
#         print(e)
#         return HttpResponseRedirect(reverse('SCMSettingurl'))
#     else:
#         host = cSCMSetting.hostname
#         rootoken = cSCMSetting.rootoken
#         gitlab = Gitlab(host, rootoken)
#     if cUser.is_superuser:
#         KList = gitlab.get_all_projects()
#         lst = SelfPaginator(request, KList, 20)
#     else:
#         fullnameid = cUser.id
#         try:
#             usertoken = SCMToken.objects.get(fullname_id=fullnameid)
#         except Exception as e:
#             print(e)
#             return HttpResponseRedirect(reverse('tokenaddurl'))
#         else:
#             usertoken = SCMToken.objects.get(fullname_id=fullnameid).usertoken
#             KList = gitlab.get_user_projects(usertoken)
#             lst = SelfPaginator(request, KList, 20)
#
#     kwvars = {
#         'lpage': lst,
#         'request': request,
#     }
#     return render_to_response('GitLab/projects.list.html', kwvars)
#
#
# @login_required
# def UploadProject(request, Url):
#     codepath = Url.split('/')[-1].split('.')[0]
#     sourcepath = SCMSetting.objects.get(id=1).sourcepath
#     sourcepath = sourcepath.rstrip('/')
#     if not os.path.exists(sourcepath):
#         os.mkdir(sourcepath)
#     if not os.path.exists(sourcepath + '/' + codepath):
#         Repo.clone_from(Url, sourcepath + '/' + codepath)
#     else:
#         os.chdir(sourcepath)
#         g = cmd.Git(codepath)
#         g.pull()
#     return HttpResponseRedirect(reverse('listallprojectsurl'))
#
#
# @login_required
# def UploadApply(request, ID, Pname, Url):
#     form = ApplyUploadForm(request.POST)
#     if form.is_valid():
#         i = ProjectApply()
#         form.save(commit=False)
#         title = form.cleaned_data['title']
#         branch = form.cleaned_data['projectbranch']
#         commitid = form.cleaned_data['commitid']
#         i.title = title
#         i.projectbranch = branch
#         i.commitid = commitid
#         i.projectname = Pname
#         i.projectid = ID
#         i.projecturl = Url
#         i.save()
#         return HttpResponseRedirect(reverse('listallprojectsurl'))
#     else:
#         form = ApplyUploadForm()
#     kwvars = {
#         'ID': ID,
#         'Pname': Pname,
#         'Url':Url,
#         'form': form,
#         'request': request,
#     }
#     return render_to_response('GitLab/project.apply.upload.html', kwvars, RequestContext(request))
#
# @login_required
# def Reset(request, Url):
#     codepath = Url.split('/')[-1].split('.')[0]
#     sourcepath = SCMSetting.objects.get(id=1).sourcepath
#     sourcepath = sourcepath.rstrip('/')
#     os.chdir(sourcepath)
#     repo = Repo(codepath)
#     repo.head.reset('HEAD~1', working_tree=1)
#     return HttpResponseRedirect(reverse('listallprojectsurl'))
#
#
# @login_required
# def GitLog(request, ID):
#     cSCMSetting = SCMSetting.objects.get(id=1)
#     host = cSCMSetting.hostname
#     rootoken = cSCMSetting.rootoken
#     gitlab = Gitlab(host, rootoken)
#     pro_Log = gitlab.get_commit_log(ID, day='30')
#     kwvars = {
#         'log': pro_Log,
#         'request': request,
#     }
#     return render_to_response('GitLab/log.list.html', kwvars)
