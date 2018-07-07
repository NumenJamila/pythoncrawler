"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

# 下面的url是连接在原来之后的，设置name,引用时用如下格式{% url 'namespace:name' param %}

app_name = 'config'
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article_page,name='article_page'),
    url(r'^edit/(?P<article_id>[0-9]+)/$', views.edit_page,name='edit_page'),
    url(r'^edit/action/$', views.edit_action,name='edit_action'),
    url(r'^del/(?P<article_id>[0-9]+)/$', views.del_page, name='del_page'),
]
