from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from student.models import *
from django.forms.extras import SelectDateWidget
from django.contrib.admin import widgets
from dira2 import settings


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
		required_css_class = 'required'
	#clean email field
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			User._default_manager.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('duplicate email')

	def clean_username(self):
		try:
			user = User.objects.get(username__iexact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError("The username already exists. Please try another one.")

	def clean_new_password1(self):
		password1 = self.cleaned_data.get('new_password1')
		if len(password1) < 6:
			raise ValidationError("Password must be at least 6 chars.")
		return password1

	#modify save() method so that we can set user.is_active to False when we first create our user
	def save(self, commit=True):        
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.is_active = False # not active until he opens activation link
			user.save()

		return user
		
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'



class UserProfileForm(forms.ModelForm):


	class Meta:
		model = UserProfile
		exclude = ("user","activation_key","key_expires","profile") 
		


	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'   


class StudentProfileForm(forms.ModelForm):


	class Meta:
		model = StudentProfile
		exclude = ("user",) 		


	def __init__(self, *args, **kwargs):
		super(StudentProfileForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'   


class EducationProfileForm(forms.ModelForm):


	class Meta:
		model = EducationProfile
		exclude = ("user",) 		


	def __init__(self, *args, **kwargs):
		super(EducationProfileForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'   			                