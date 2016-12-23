from django.conf.urls import url
from views import *

urlpatterns = [
                       url(r"^projectgroup/add/$", project_group_add, name="project_group_add"),
                       url(r"^projectgroup/list/$", project_group_list, name="project_group_list"),
                       url(r"^projectgroup/del/$", project_group_del, name="project_group_del"),
                       url(r"^projectgroup/edit/$", project_group_edit, name="project_group_edit"),
                       url(r"^project/add/$", project_add, name="project_add"),
                       url(r"^project/del/$", project_del, name="project_del"),
                       url(r"^project/list/$", project_list, name="project_list"),
                       url(r"^project/edit/$", project_edit, name="project_edit"),
                       url(r"^projectenv/add/$", project_env_add, name="project_env_add"),
                       url(r"^projectenv/list/$", project_env_list, name="project_env_list"),
                       url(r"^projectenv/edit/$", project_env_edit, name="project_env_edit"),
                       url(r"^projectenv/del/$", project_env_del, name="project_env_del"),

                       ]
