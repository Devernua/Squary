# coding: utf-8
import datetime
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic

from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from django.core.files.uploadedfile import SimpleUploadedFile

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import User, Image, Comment, Rating
from . import forms

class IndexView(generic.ListView):
	template_name = 'posts/index.html'
	context_object_name = 'latest_image_list'

	def get_queryset(self):
		return Image.objects.order_by('-pdate')[:5]

class DetailView(generic.DetailView):
	model = Image
	template_name = 'posts/detail.html'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		context['form'] = forms.CommentForm()
		return context

class CreateImage(FormView):
	template_name = 'posts/create.html'
	form_class = forms.ImageForm
	success_url = 'posts/create/result'

class RegisterFormView(FormView):
	form_class = forms.RegistrationForm
	success_url = "posts/login/"
	template_name = "posts/signup.html"

def add_user(request):
	form = forms.RegistrationForm()
	if request.method == 'POST':
		form = forms.RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			u = User.objects.create_user(
				username 	= cd['username'],
				email 		= cd['email'],
				password 	= cd['password1'],
				avatar		= cd['avatar'],
			)


			u.save()
			return HttpResponseRedirect(reverse('posts:login') )
	return render(request, 'posts/signup.html', {
		'error_message': "Sorry",
		'form' : form,
	})

def add_image(request):
	form = forms.ImageForm()
	if request.method == "POST":
		form = forms.ImageForm(request.POST, request.FILES)
		if form.is_valid():
			img = Image(img = form.cleaned_data['img'])
			img.author = request.user
			img.pdate = timezone.now()
			img.name = ""
			img.save()
			return HttpResponseRedirect(reverse('posts:index') )
	return render(request, 'posts/create.html', {
		'error_message': "You didn't enter image.",
		'form':form,
		})

def add_comment(request, image_id):
	p = get_object_or_404(Image, pk = image_id)
	form = forms.CommentForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		com = Comment(image = p, text = form.cleaned_data['text'])
		com.author = request.user
		com.pdate = timezone.now()
		com.save()
		return HttpResponseRedirect(reverse('posts:detail', args=(p.id,)))
	return render(request, 'posts/detail.html', {
		'image':p,
		'error_message': "You didn't enter comment.",
		'form':form,
})

def add_rating(request, image_id):
	p = get_object_or_404(Image, pk = image_id)
	if request.method == "POST":
		try:
			rt = Rating.objects.get(user = request.user, img=p)
			rt.delete();
		except Rating.DoesNotExist:
			rt = Rating(img=p)
			rt.user = request.user
			rt.save()
			return HttpResponseRedirect(reverse('posts:detail', args=(p.id,)))
	return render(request, 'posts/detail.html', {
		'image': p,
	})

class UserUpdate(UpdateView):
    form_class = forms.RegistrationForm
    model = User
    template_name = 'singup.html'
    success_url = '/user/edit/success/'
