from django.contrib import admin
from models import *
import datetime

from django.http import HttpResponse
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Register your models here.


class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "age",'id_no', 'religion','address','marital_status')

class EducationProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "name_of_educational_institutional_or_schools",'qualification_level', 'description')


admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(EducationProfile, EducationProfileAdmin)	
