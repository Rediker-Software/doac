from django.test import TestCase
from doac.models import AuthorizationCode, AuthorizationToken, Client, RedirectUri, Scope
import urllib


class OAuthTestCase(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")

        self.oauth_client = Client(name="Test Client", access_host="http://localhost/")
        self.oauth_client.save()

        self.scope = Scope(short_name="test", full_name="Test Scope", description="This is a test scope.")
        self.scope.save()

    def assertExceptionRendered(self, request, exception):
        self.assertEquals(request.content, exception.reason)
        self.assertEquals(request.status_code, 401)

    def assertExceptionJson(self, request, exception):
        try:
            import simplejson as json
        except ImportError:
            import json

        data = {
            "error": exception.error,
            "error_description": exception.reason,
        }

        self.assertEquals(request.content, json.dumps(data))
        self.assertEquals(request.status_code, getattr(exception, 'code', 400))

    def assertExceptionRedirect(self, request, exception):
        params = {
            "error": exception.error,
            "error_description": exception.reason,
            "state": "o2cs",
        }

        url = self.redirect_uri.url + "?" + urllib.urlencode(params)

        self.assertRedirects(request, url)
        self.assertEquals(request.status_code, 302)


class ApprovalTestCase(OAuthTestCase):

    def setUp(self):
        super(ApprovalTestCase, self).setUp()

        self.redirect_uri = RedirectUri(client=self.oauth_client, url="http://localhost/redirect_endpoint/")
        self.redirect_uri.save()

        self.authorization_code = AuthorizationCode(client=self.oauth_client, redirect_uri=self.redirect_uri)
        self.authorization_code.save()

        self.authorization_code.scope = [self.scope]
        self.authorization_code.save()


class AuthorizeTestCase(OAuthTestCase):

    def setUp(self):
        super(AuthorizeTestCase, self).setUp()

        self.redirect_uri = RedirectUri(client=self.oauth_client, url="http://localhost/redirect_endpoint/")
        self.redirect_uri.save()


class TokenTestCase(OAuthTestCase):

    def setUp(self):
        super(TokenTestCase, self).setUp()

        self.client_secret = self.oauth_client.secret

        self.authorization_token = AuthorizationToken(user=self.user, client=self.oauth_client)
        self.authorization_token.save()

        self.authorization_token.scope = [self.scope]
        self.authorization_token.save()


class DecoratorTestCase(OAuthTestCase):

    def setUp(self):
        from django.http import HttpRequest
        from doac.middleware import AuthenticationMiddleware

        super(DecoratorTestCase, self).setUp()

        self.client_secret = self.oauth_client.secret

        self.authorization_token = AuthorizationToken(user=self.user, client=self.oauth_client)
        self.authorization_token.save()

        self.authorization_token.scope = [self.scope]
        self.authorization_token.save()

        self.authorization_token.generate_refresh_token()
        self.authorization_token.refresh_token.generate_access_token()

        self.access_token = self.authorization_token.refresh_token.access_tokens.all()[0]

        self.request = HttpRequest()
        self.mw = AuthenticationMiddleware()


class MiddlewareTestCase(OAuthTestCase):

    def setUp(self):
        from django.test.client import RequestFactory

        self.factory = RequestFactory()
