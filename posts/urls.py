# coding: utf-8
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^post/user/(?P<pk>[0-9]+)/$', views.UserIndexView.as_view(), name='index_user'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^post/(?P<image_id>[0-9]+)/comment/$', login_required(views.add_comment), name='comment'),
	url(r'^post/(?P<image_id>[0-9]+)/rating/$', login_required(views.add_rating), name='rating'),
	url(r'^signup/$', views.RegisterFormView.as_view(), name='signup'),
	url(r'^signup/result/$', views.add_user, name='add_user'),
	url(r'^login/', login, {'template_name': 'posts/login.html'}, name='login'),
	url(r'^logout/', logout, {'template_name': 'posts/logout.html'}, name='logout'),
	url(r'^post/create$', login_required(views.CreateImage.as_view()), name='create'),
	url(r'^post/create/result/$', views.add_image, name='add_image'),
	url(r'^edit/$', login_required(views.UpdateUserFormView.as_view()), name='settings'),
	url(r'^edit/result/$', login_required(views.update_user), name='user_edit'),
	url(r'^post/search/$', views.do_search, name='search'),

]
