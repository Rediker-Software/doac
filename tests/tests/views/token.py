from django.core.urlresolvers import reverse
from ..test_cases import TokenTestCase


class TestErrors(TokenTestCase):
    
    def test_grant_type(self):
        from oauth2_consumer.exceptions.unsupported_grant_type import GrantTypeNotProvided, GrantTypeNotValid
        
        request = self.client.post(reverse("oauth2_token"))
        self.assertExceptionJson(request, GrantTypeNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": ""})
        self.assertExceptionJson(request, GrantTypeNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "invalid"})
        self.assertExceptionJson(request, GrantTypeNotValid())
    
    def test_client_id(self):
        from oauth2_consumer.exceptions.invalid_request import ClientNotProvided
        from oauth2_consumer.exceptions.invalid_client import ClientDoesNotExist
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code"})
        self.assertExceptionJson(request, ClientNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": ""})
        self.assertExceptionJson(request, ClientNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": 1234})
        self.assertExceptionJson(request, ClientDoesNotExist())
    
    def test_client_secret(self):
        from oauth2_consumer.exceptions.invalid_client import ClientSecretNotValid
        from oauth2_consumer.exceptions.invalid_request import ClientSecretNotProvided
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id})
        self.assertExceptionJson(request, ClientSecretNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": ""})
        self.assertExceptionJson(request, ClientSecretNotProvided())
        
        request = self.client.post(reverse("oauth2_token"), {"grant_type": "authorization_code", "client_id": self.oauth_client.id, "client_secret": "notVerySecret"})
        self.assertExceptionJson(request, ClientSecretNotValid())
