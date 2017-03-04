"""codeshastra3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^superuser/', admin.site.urls),
    url(r'^admin/', views.honey_pot),
    url(r'^$', views.home),
    url(r'^heatmap/(\d+)$', views.alt_heatmap),
    url(r'^getlocation/', views.get_location),
    url(r'^disaster/(\d+)$', views.disaster_information),
    url(r'^suggest/(\d+)$', views.suggest),
    url(r'^monitor/$',views.monitor),
    url(r'^test/',views.test),
    url(r'^monitorcenter/(\d+)$', views.monitor_center),
    url(r'^hospitalportal/(\d+)$', views.hospital_portal),
    url(r'^upload/$', views.upload),
    url(r'^find_missing_person/$', views.find_missing_person),
    url(r'^classifier/', include('classifier.urls')),
    url(r'^saveVictim/$', views.save_victim),
    url(r'^seed/(\d+)$', views.test_suggest),
    url(r'^attackers/$', views.attackers),
    url(r'^hospedit/(\d+)$', views.hospital_edit),
    #url(r'^clean/$', views.cleanup),

]
