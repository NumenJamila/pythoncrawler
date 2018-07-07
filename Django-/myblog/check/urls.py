from django.conf.urls import url
from . import views

# 下面的url是连接在原来之后的，设置name,引用时用如下格式{% url 'namespace:name' param %}

app_name = 'check'
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article_page,name='article_page'),
    url(r'^edit/(?P<article_id>[0-9]+)/$', views.edit_page,name='edit_page'),
    url(r'^edit/action/$', views.edit_action,name='edit_action'),
    url(r'^del/(?P<article_id>[0-9]+)/$', views.del_page, name='del_page'),
]