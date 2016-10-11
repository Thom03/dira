from django.shortcuts import render
from rest_framework import status
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.views import generic
import hashlib, datetime, random
from django.utils import timezone
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.core import serializers
from student.models import *
from student.forms import *
from dira2 import settings
from django.utils.decorators import method_decorator
import os
from django.views.generic.base import TemplateView
import uuid
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.contrib.auth import logout
from django.contrib.auth import views
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth import get_user_model





def index(request):
    return render(request, 'home.html')


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up.\n Password is: %s\n To activate your account, click this link within 48hours https://localhost:8000/confirm/%s" % (username, password, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/register/')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('register.html', args, context_instance=RequestContext(request))

def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        messages.error(request, 'Account activation period has expired.Please register  account again!')
        return render_to_response('confirm_expired.html')
    
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('confirm.html')


def user_login(request):
    next = request.GET.get('next', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':

        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)

            else:
                messages.error(request, "User does not exist.Check your email to activate account! or register account")
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Invalid username or password.Please try again!")
            return HttpResponseRedirect(reverse("login"))

    return render(request, 'login.html', {'redirect_to':next})

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')




class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        StudentProfile.objects.get_or_create(user=self.request.user)
        return user 

class EducationProfileDetailView(ListView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(EducationProfileDetailView, self).get_object(queryset)
        EducationProfile.objects.get_or_create(user=self.request.user)
        return user         
        

class UserProfileEditView(UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return StudentProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("user_profile", kwargs={'slug': self.request.user})
        

class EducationProfileEditView(UpdateView):
    model = EducationProfile
    form_class = EducationProfileForm
    template_name = "edit_education.html"

    def get_object(self, queryset=None):
        return EducationProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("user_profile", kwargs={'slug': self.request.user})