from django import forms
from .models import User

class ImageForm(forms.Form):
	img = forms.ImageField(required=True)

class CommentForm(forms.Form):
	text = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))

class RegistrationForm(forms.Form):
	username 	= forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	password1 	= forms.CharField(label=u'password', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
	password2 	= forms.CharField(label=u'again', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
	email 		= forms.EmailField(max_length = 200, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	avatar 		= forms.ImageField(required=True)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username = username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(('duplicate_username'), code='duplicate_username')

	def clean(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if (password1 == password2):
			return self.cleaned_data
		else:
			raise forms.ValidationError(('enter password again'), code='invalid_password')
