from django.conf.urls import patterns, include, url
from oauth2_consumer import urls as oauth_urls
from . import views

urlpatterns = patterns('',
    url(r"^oauth/", include(oauth_urls)),
    
    url(r"^no_args/", views.no_args, name="no_args"),
)
