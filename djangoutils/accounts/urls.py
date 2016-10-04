from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from djangoutils.accounts.forms import AuthenticationForm

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'authentication_form': AuthenticationForm}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='login'),
    (r'', include('social_auth.urls')),
    (r'', include('registration.urls')),
)
