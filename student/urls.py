from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from views import *
from forms import *
from django.contrib.auth.decorators import login_required as auth

urlpatterns = [

	url(r'^$', 'student.views.index', name='index'),
	url(r'^register/$', 'student.views.register_user', name='register_user'),
	url(r'^confirm/(?P<activation_key>\w+)/', 'student.views.register_confirm', name='register_confirm'),
	url(r'^accounts/login/$', 'student.views.user_login', name='login'),
    url(r'^accounts/logout/', 'student.views.user_logout', name='logout'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^password/$', 'django.contrib.auth.views.password_reset', {}, 'password_reset'),
    url(r'^accounts/password_change/$','django.contrib.auth.views.password_change', 
        {'post_change_redirect' : '/accounts/password_change/done/'}, 
        name="password_change"), 
    url(r'^accounts/password_change/done/$','django.contrib.auth.views.password_change_done'),
    url(r'^accounts/password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password_reset/mailed/'},
        name="password_reset"),
    url(r'^accounts/password_reset/mailed/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password_reset/complete/'}),
    url(r'^accounts/password_reset/complete/$', 
        'django.contrib.auth.views.password_reset_complete'),


    url(r'^users/(?P<slug>\w+)$', UserProfileDetailView.as_view(), name='user_profile'),
    url(r'^users/(?P<slug>\w+)$', EducationProfileDetailView.as_view(), name='education_profile'),
    url(r'^edit_profile/$', auth(UserProfileEditView.as_view()), name="edit_profile"),
     url(r'^edit_education/$', auth(EducationProfileEditView.as_view()), name="edit_education"),





]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
