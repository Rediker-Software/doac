try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r"^authorize/$", views.AuthorizeView.as_view(), name="oauth2_authorize"),
    url(r"^approval/$", views.ApprovalView.as_view(), name="oauth2_approval"),
    url(r"^token/$", views.TokenView.as_view(), name="oauth2_token"),
)
