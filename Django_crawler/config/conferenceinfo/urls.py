from django.conf.urls import url
from . import views

# 下面的url是连接在原来之后的，设置name,引用时用如下格式{% url 'namespace:name' param %}

app_name = 'conferenceinfo'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^conference/(?P<conference_id>[0-9]+)/$', views.conference_page,name='conference_page'),
    url(r'^edit/(?P<conference_id>[0-9]+)/$', views.edit_page,name='edit_page'),
    url(r'^edit/action/$', views.edit_action,name='edit_action'),
    url(r'^del/(?P<conference_id>[0-9]+)/$', views.del_page, name='del_page'),
    url(r'^configfile/$', views.configfile, name='configfile'),
    url(r'^newconference/$', views.newconference, name='newconference'),
    url(r'^space_data/$', views.space_data, name='space_data'),
    url(r'^space/$', views.space, name='space'),
]
