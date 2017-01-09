from django.conf.urls import url
from views import *

urlpatterns = [
                       url(r"^getProject/$", getProject, name="getProject"),
                       url(r"^projectgroup/add/$", project_group_add, name="project_group_add"),
                       url(r"^projectgroup/list/$", project_group_list, name="project_group_list"),
                       url(r"^projectgroup/del/$", project_group_del, name="project_group_del"),
                       url(r"^projectgroup/edit/$", project_group_edit, name="project_group_edit"),
                       url(r"^project/add/$", project_add, name="project_add"),
                       url(r"^project/del/$", project_del, name="project_del"),
                       url(r"^project/list/$", project_list, name="project_list"),
                       url(r"^project/edit/$", project_edit, name="project_edit"),
                       url(r"^projectconfig/add/$", project_config_add, name="project_config_add"),
                       url(r"^projectconfig/list/$", project_config_list, name="project_config_list"),
                       url(r"^projectconfig/edit/$", project_config_edit, name="project_config_edit"),
                       url(r"^projectconfig/del/$", project_config_del, name="project_config_del"),
                       url(r"^env/add/$", env_add, name="env_add"),
                       url(r"^env/list/$", env_list, name="env_list"),
                       url(r"^env/edit/$", env_edit, name="env_edit"),
                       url(r"^env/del/$", env_del, name="env_del"),
                       url(r"^publsihconfig/add/$", publish_config_add, name="publish_config_add"),
                       url(r"^publsihconfig/list/$", publish_config_list, name="publish_config_list"),
                       url(r"^publsihconfig/edit/$", publish_config_edit, name="publish_config_edit"),
                       url(r"^publsihconfig/del/$", publish_config_del, name="publish_config_del"),
                       ]
