from django.core.urlresolvers import reverse
from ..test_cases import TokenTestCase
try:
    import simplejson as json
except ImportError:
    import json


class TestTokenErrors(TokenTestCase):

    def test_grant_type(self):
        from doac.exceptions.unsupported_grant_type import \
            GrantTypeNotProvided, GrantTypeNotValid

        data = {}

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, GrantTypeNotProvided())

        data["grant_type"] = ""

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, GrantTypeNotProvided())

        data["grant_type"] = "invalid"

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, GrantTypeNotValid())

    def test_client_id(self):
        from doac.exceptions.invalid_request import ClientNotProvided
        from doac.exceptions.invalid_client import ClientDoesNotExist

        data = {
            "grant_type": "authorization_code",
        }

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, ClientNotProvided())

        data["client_id"] = ""

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, ClientNotProvided())

        data["client_id"] = "1234"

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, ClientDoesNotExist())

    def test_client_secret(self):
        from doac.exceptions.invalid_client import ClientSecretNotValid
        from doac.exceptions.invalid_request import ClientSecretNotProvided

        data = {
            "grant_type": "authorization_code",
            "client_id": self.oauth_client.id,
        }

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, ClientSecretNotProvided())

        data["client_secret"] = ""

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, ClientSecretNotProvided())

        data["client_secret"] = "notVerySecret"

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, ClientSecretNotValid())

    def test_code(self):
        from doac.exceptions.invalid_request import \
            AuthorizationCodeAlreadyUsed, AuthorizationCodeNotProvided, \
            AuthorizationCodeNotValid

        data = {
            "grant_type": "authorization_code",
            "client_id": self.oauth_client.id,
            "client_secret": self.client_secret,
        }

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, AuthorizationCodeNotProvided())

        data["code"] = ""

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, AuthorizationCodeNotProvided())

        data["code"] = "invalid"

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, AuthorizationCodeNotValid())

        data["code"] = self.authorization_token.token

        request = self.client.post(reverse("oauth2_token"), data)
        request = self.client.post(reverse("oauth2_token"), data)

        self.assertExceptionJson(request, AuthorizationCodeAlreadyUsed())

    def test_refresh_token(self):
        from doac.exceptions.invalid_request import \
            RefreshTokenNotProvided, RefreshTokenNotValid

        data = {
            "grant_type": "refresh_token",
            "client_id": self.oauth_client.id,
            "client_secret": self.client_secret,
        }

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, RefreshTokenNotProvided())

        data["refresh_token"] = ""

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, RefreshTokenNotProvided())

        data["refresh_token"] = "invalid"

        request = self.client.post(reverse("oauth2_token"), data)
        self.assertExceptionJson(request, RefreshTokenNotValid())


class TestTokenResponse(TokenTestCase):

    def test_authorization_token(self):
        data = {
            "grant_type": "authorization_code",
            "client_id": self.oauth_client.id,
            "client_secret": self.client_secret,
            "code": self.authorization_token.token,
        }

        request = self.client.post(reverse("oauth2_token"), data)

        refresh_token = self.authorization_token.refresh_token
        access_token = refresh_token.access_tokens.all()[0]

        response = {
            "refresh_token": refresh_token.token,
            "token_type": "bearer",
            "expires_in": 5183999,
            "access_token": access_token.token,
        }

        self.assertEqual(request.content, json.dumps(response))
        self.assertEqual(request.status_code, 200)

    def test_refresh_token(self):
        refresh_token = self.authorization_token.generate_refresh_token()

        data = {
            "grant_type": "refresh_token",
            "client_id": self.oauth_client.id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token.token,
        }

        request = self.client.post(reverse("oauth2_token"), data)

        response = {
            "token_type": "bearer",
            "expires_in": 7199,
            "access_token": refresh_token.access_tokens.all()[0].token,
        }

        self.assertEqual(request.content, json.dumps(response))
        self.assertEqual(request.status_code, 200)

    def test_password(self):
        from doac.models import RefreshToken

        data = {
            "grant_type": "password",
            "client_id": self.oauth_client.id,
            "client_secret": self.client_secret,
            "username": self.user.username,
            "password": "test",
        }

        request = self.client.post(reverse("oauth2_token"), data)

        self.assertEqual(RefreshToken.objects.count(), 1)

        refresh_token = RefreshToken.objects.get()
        access_token = refresh_token.access_tokens.get()

        self.assertEqual(request.status_code, 200)

        response = {
            "token_type": "bearer",
            "expires_in": 7199,
            "refresh_token": refresh_token.token,
            "access_token": access_token.token,
        }

        self.assertEqual(request.content, json.dumps(response))
