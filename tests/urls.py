try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url

from oauth2_consumer import urls as oauth_urls
from . import views

urlpatterns = patterns('',
    url(r"^oauth/", include(oauth_urls)),
    
    url(r"^no_args/", views.no_args, name="no_args"),
    url(r"^has_scope/", views.has_scope, name="has_scope"),
    url(r"^scope_doesnt_exist/", views.scope_doesnt_exist, name="scope_doesnt_exist"),
    url(r"^doesnt_have_all_scope/", views.doesnt_have_all_scope, name="doesnt_have_all_scope"),
)
