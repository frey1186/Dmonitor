"""MyMonitor URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from monitor import views

app_name = 'monitor'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^host/$', views.host_list, name='host_list'),
    url(r'hosts/(\d+)/$', views.host_detail, name='host_detail'),

    url(r'^images/$', views.images_list, name='images_list'),
    url(r'^container/$', views.container_list, name='container_list'),
    url(r'hosts/(\d+)/container/(\S+)/$', views.container_detail, name='container_detail'),

    url(r'^real_host/$', views.real_host, name='real_host'),
    url(r'^hosts/(\d+)/real_data_detail/$', views.real_data_detail, name='real_data_detail'),
    url(r'^hosts/(\d+)/current/data/$', views.current_data,name='current_data'),
    url(r'^hosts/(\d+)/monitor_data_detail/$', views.monitor_data_detail, name='monitor_data_detail'),
    url(r'^hosts/(\d+)/monitor/data/$', views.monitor_data, name='monitor_data'),

]
