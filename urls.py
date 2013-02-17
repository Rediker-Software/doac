from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r"^authorize/$", views.AuthorizeView.as_view(), name="oauth2_authorize"),
    url(r"^approval/$", views.AuthorizeView.as_view(), name="oauth2_approval"),
    
    url(r"^redirect_endpoint/$", views.redirect_endpoint, name="oauth2_redirect_endpoint"),
)
