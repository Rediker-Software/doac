from django.conf.urls import patterns, include, url
from oauth2_consumer import urls as oauth_urls

urlpatterns = patterns('',
    url(r"^oauth/", include(oauth_urls)),
)
