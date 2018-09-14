from django.conf.urls import url
from . import views

# 下面的url是连接在原来之后的，设置name,引用时用如下格式{% url 'namespace:name' param %}

app_name = 'setconfig'
urlpatterns = [
    url(r'^index/$', views.index,name='index'),
    url(r'^conf/(?P<conf_id>[0-9]+)/$', views.setconfig_page,name='setconfig_page'),
    url(r'^edit/(?P<conf_id>[0-9]+)/$', views.edit_page,name='edit_page'),
    url(r'^edit/action/$', views.edit_action,name='edit_action'),
    url(r'^del/(?P<conf_id>[0-9]+)/$', views.del_page, name='del_page'),
    url(r'^newconfigfile/$', views.newconfigfile,name='newconfigfile'),
    url(r'^check/(?P<conf_id>[0-9]+)/$', views.check,name='check'),
    url(r'^input/(?P<conf_id>[0-9]+)/$', views.input,name='input'),
    url(r'^search/$', views.search, name='search'),
]
