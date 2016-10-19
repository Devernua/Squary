# coding: utf-8
import datetime
from django.utils import timezone
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.mail import send_mail

from django.core.files.uploadedfile import SimpleUploadedFile

from .models import User, Image, Comment

class IndexView(generic.ListView):
	template_name = 'posts/index.html'
	context_object_name = 'latest_image_list'

	def get_queryset(self):
		return Image.objects.order_by('-pdate')[:5]

class DetailView(generic.DetailView):
	model = Image
	template_name = 'posts/detail.html'

