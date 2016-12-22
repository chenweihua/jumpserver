from django.conf.urls import  include, url
from views import index,skin_config,Login,Logout,upload,exec_cmd,setting,web_terminal,download

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^skin_config/$', skin_config, name='skin_config'),
    url(r'^login/$', Login, name='login'),
    url(r'^logout/$', Logout, name='logout'),
    url(r'^exec_cmd/$', exec_cmd, name='exec_cmd'),
    url(r'^file/upload/$', upload, name='file_upload'),
    url(r'^file/download/$', download, name='file_download'),
    url(r'^setting', setting, name='setting'),
    url(r'^terminal/$', web_terminal, name='terminal'),
    url(r'^juser/', include('juser.urls')),
    url(r'^jasset/', include('jasset.urls')),
    url(r'^jlog/', include('jlog.urls')),
    url(r'^jperm/', include('jperm.urls'))
]
