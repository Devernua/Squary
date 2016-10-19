# coding: utf-8
#from django.contrib.auth.views import login, logout
from django.conf.urls import url
from . import views
#from django.contrib.auth.decoratorss import login_required

urlpatterns = [
		url(r'^$', views.IndexView.as_view(), name='index'),
		url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
		] 
