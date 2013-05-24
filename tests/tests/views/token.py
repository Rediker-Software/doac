from django.core.urlresolvers import reverse
from ..test_cases import TokenTestCase
try:
    import simplejson as json
except ImportError:
    import json


class TestTokenErrors(TokenTestCase):
    
    def test_grant_type(self):
        from doac.exceptions.unsupported_grant_type import GrantTypeNotProvided, GrantTypeNotValid
        
        request = self.client.post(reverse("oauth2_token"))
        self.assertExceptionJson(request, GrantTypeNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": ""})
        self.assertExceptionJson(request, GrantTypeNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "invalid"})
        self.assertExceptionJson(request, GrantTypeNotValid())
    
    def test_client_id(self):
        from doac.exceptions.invalid_request import ClientNotProvided
        from doac.exceptions.invalid_client import ClientDoesNotExist
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code"})
        self.assertExceptionJson(request, ClientNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": ""})
        self.assertExceptionJson(request, ClientNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": 1234})
        self.assertExceptionJson(request, ClientDoesNotExist())
    
    def test_client_secret(self):
        from doac.exceptions.invalid_client import ClientSecretNotValid
        from doac.exceptions.invalid_request import ClientSecretNotProvided
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id})
        self.assertExceptionJson(request, ClientSecretNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": ""})
        self.assertExceptionJson(request, ClientSecretNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": "notVerySecret"})
        self.assertExceptionJson(request, ClientSecretNotValid())
    
    def test_code(self):
        from doac.exceptions.invalid_request import AuthorizationCodeAlreadyUsed, AuthorizationCodeNotProvided, AuthorizationCodeNotValid
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": self.client_secret})
        self.assertExceptionJson(request, AuthorizationCodeNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": self.client_secret, "code": ""})
        self.assertExceptionJson(request, AuthorizationCodeNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": self.client_secret, "code": "invalid"})
        self.assertExceptionJson(request, AuthorizationCodeNotValid())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": self.client_secret, "code": self.authorization_token.token})
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": self.client_secret, "code": self.authorization_token.token})
        self.assertExceptionJson(request, AuthorizationCodeAlreadyUsed())
    
    def test_refresh_token(self):
        from doac.exceptions.invalid_request import RefreshTokenNotProvided, RefreshTokenNotValid
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "refresh_token", "client_id": self.oauth_client.id, "client_secret": self.client_secret})
        self.assertExceptionJson(request, RefreshTokenNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "refresh_token", "client_id": self.oauth_client.id, "client_secret": self.client_secret, "refresh_token": ""})
        self.assertExceptionJson(request, RefreshTokenNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "refresh_token", "client_id": self.oauth_client.id, "client_secret": self.client_secret, "refresh_token": "invalid"})
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
        
        response = {
            "refresh_token": self.authorization_token.refresh_token.token,
            "token_type": "bearer",
            "expires_in": 5183999,
            "access_token": self.authorization_token.refresh_token.access_tokens.all()[0].token,
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
