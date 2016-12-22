from django.conf.urls import url
from views import *

urlpatterns = [
                       url(r"^projectgroup/add/$", project_group_add, name="project_group_add"),
                       url(r"^projectgroup/list/$", project_group_list, name="user_group_list"),
                       url(r"^projectgroup/del/$", project_group_del, name="user_group_del"),
                       url(r"^projectgroup/edit/$", project_group_edit, name="user_group_edit"),
                       url(r"^project/add/$", project_add, name="user_add"),
                       url(r"^project/del/$", project_del, name="user_del"),
                       url(r"^project/list/$", project_list, name="user_list"),
                       url(r"^project/edit/$", project_edit, name="user_edit"),
                       # url(r"^project/detail/$", project_detail, name="user_detail"),
                       # url(r"^project/profile/$", project_profile, name="user_profile"),
                       # url(r"^project/update/$", project_info, name="user_update"),

                       ]
