from __future__ import unicode_literals
from django.db import models
import datetime 
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import signals
from django.contrib.gis.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from django.core.validators import MaxLengthValidator,MinLengthValidator, RegexValidator
from django.db.models import Max
from dira2 import settings
from django.utils.safestring import mark_safe  


class UserProfile(models.Model):

	SEX_CHOICES = (
		('F', 'Female',),
		('M', 'Male',),
		('U', 'Unsure',),
	)

	MAR_CHOICES = (
		('S', 'Single',),
		('M', 'Married',),
		
	)


	user = models.OneToOneField(User)	
	photo = models.ImageField(upload_to = 'media_root/', blank=True, null=True)
	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField(null=True, blank=True)
	sex = models.CharField(max_length=1, choices=SEX_CHOICES,)
	age = models.PositiveIntegerField(blank=True,null=True)
	religion = models.CharField(max_length=50, blank=True, null=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	website = models.CharField(max_length=50, null=True, blank=True)
	industry_or_course = models.CharField(max_length=50, null=True, blank=True)
	id_no = models.CharField(max_length=255,blank=True,null=True)	  
	phone_no = models.CharField(max_length=255,blank=True,null=True)
	profile = models.TextField(max_length=256, null=True,blank=True)
	special_interest_or_SH = models.CharField(max_length=50,blank=True, null=True)      
	address = models.CharField(max_length=255,blank=True,null=True)
	marital_status = models.CharField(max_length=50, choices=MAR_CHOICES, blank=True,null=True)
	

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name_plural = "User Profiles"

	def get_url(self):
		url = self.url
		if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
			url = "http://" + str(self.url)
		return url 

	def get_screen_name(self):
		try:
			if self.user.get_full_name():
				return self.user.get_full_name()
			else:
				return self.user.username
		except:
			return self.user.username   

def create_user_profile(sender, instance, created, **kwargs):
	if created == True:
		p = UserProfile()
		p.user = instance
		p.save()


class StudentProfile(models.Model):

	SEX_CHOICES = (
		('F', 'Female',),
		('M', 'Male',),
		('U', 'Unsure',),
	)

	MAR_CHOICES = (
		('S', 'Single',),
		('M', 'Married',),
		
	)

	user = models.OneToOneField(User)
	sex = models.CharField(max_length=1, choices=SEX_CHOICES,)
	age = models.PositiveIntegerField(blank=True,null=True)
	religion = models.CharField(max_length=50, blank=True, null=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	website = models.CharField(max_length=50, null=True, blank=True)
	industry_or_course = models.CharField(max_length=50, null=True, blank=True)
	id_no = models.CharField(max_length=255,blank=True,null=True)	  
	phone_no = models.CharField(max_length=255,blank=True,null=True)	
	special_interest_or_SH = models.CharField(max_length=50,blank=True, null=True)      
	address = models.CharField(max_length=255,blank=True,null=True)
	marital_status = models.CharField(max_length=50, choices=MAR_CHOICES, blank=True,null=True)
	photo = models.ImageField(upload_to = 'media_root/', blank=True, null=True)


	def __str__(self):
		return self.user.user

	class Meta:
		verbose_name_plural = "Student Profiles"


	def get_screen_name(self):
		try:
			if self.user.get_full_name():
				return self.user.get_full_name()
			else:
				return self.user.username
		except:
			return self.user.username  		



class EducationProfile(models.Model):

	QUL_CHOICES = (
		('M', 'Masters',),
		('B', 'Bachelors',),
		('D', 'Diploma',),
		('C', 'Certificate',),
	)
	user = models.OneToOneField(User)
	name_of_educational_institutional_or_schools = models.CharField(max_length=50)
	qualification_level =  models.CharField(max_length=50, choices=QUL_CHOICES)
	start_date = models.DateField(auto_now_add=False,null=True)
	end_date = models.DateField(auto_now_add=False,null=True)
	description = models.TextField()


	def __str__(self):
		return self.user.name_of_educational_institutional_or_schools


	class Meta:
		verbose_name_plural = "Education Profiles"	


	def get_screen_name(self):
		try:
			if self.user.get_full_name():
				return self.user.get_full_name()
			else:
				return self.user.username
		except:
			return self.user.username   	


	

	

	