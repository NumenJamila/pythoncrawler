from django.conf.urls import url,include # 增加了include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^setconfig/',include('setconfig.urls',namespace='setconfig')), # 使用include后，指定namespace
    url(r'^conferenceinfo/',include('conferenceinfo.urls',namespace='conferenceinfo')), # 使用include后，指定namespace
    url(r'^multiconfig/',include('multiconfig.urls',namespace='multiconfig')),
]



