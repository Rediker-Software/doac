# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    # For Django ≥ 1.4.
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse
from django.utils import unittest
try:
    import rest_framework
except ImportError:
    rest_framework = None
if rest_framework:
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.views import APIView

    from doac.contrib.rest_framework.authentication import DoacAuthentication
from ..test_cases import TokenTestCase


if rest_framework:
    class MockView(APIView):
        authentication_classes = (DoacAuthentication,)

        def get(self, request):
            return HttpResponse('foo')

    urlpatterns = patterns(
        '',
        url(r'^anonymous/$', MockView.as_view()),
        url(r'^authenticated-only/$', MockView.as_view(permission_classes=(IsAuthenticated,))),
    )


@unittest.skipUnless(rest_framework, 'Django Rest Framework is not installed.')
class RestFrameworkTestCase(TokenTestCase):
    urls = 'tests.tests.contrib.rest_framework_tests'

    def setUp(self):
        super(RestFrameworkTestCase, self).setUp()
        self.authorization_token.generate_refresh_token()
        self.access_token = self.authorization_token.refresh_token.generate_access_token()

    def test_anonymous_users_are_not_assaulted(self):
        """Ensure that if an user doesn’t make an attempt to authenticate, 401 Unauthorized isn’t returned."""
        response = self.client.get('/anonymous/')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_users_are_not_authenticated(self):
        """Ensure that authentication isn’t performed if an user doesn’t make an attempt to do it."""
        response = self.client.get('/authenticated-only/')
        self.assertEqual(response.status_code, 401)

    def test_invalid_credentials_are_not_authenticated(self):
        """Ensure that 401 Unauthorized response is returned when user fails in authentication attempt."""
        response = self.client.get('/anonymous/', HTTP_AUTHORIZATION='Bearer {0}'.format('invalid-token'))
        self.assertEqual(response.status_code, 401)

    def test_valid_credentials_are_authenticated(self):
        """Ensure that if user provides valid credentials, he is authorized."""
        response = self.client.get('/authenticated-only/', HTTP_AUTHORIZATION='Bearer {0}'.format(self.access_token))
        self.assertEqual(response.status_code, 200)
