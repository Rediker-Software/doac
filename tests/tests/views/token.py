from ..test_cases import TokenTestCase


class TestErrors(TokenTestCase):
    
    def test_grant_type(self):
        from oauth2_consumer.exceptions.unsupported_grant_type import GrantTypeNotProvided, GrantTypeNotValid
        
        request = self.client.post("/oauth/token/")
        self.assertExceptionJson(request, GrantTypeNotProvided())
        
        request = self.client.post("/oauth/token/", {"grant_type": ""})
        self.assertExceptionJson(request, GrantTypeNotProvided())
        
        request = self.client.post("/oauth/token/", {"grant_type": "invalid"})
        self.assertExceptionJson(request, GrantTypeNotValid())
    
    def test_client_id(self):
        from oauth2_consumer.exceptions.invalid_request import ClientNotProvided
        from oauth2_consumer.exceptions.invalid_client import ClientDoesNotExist
        
        request = self.client.post("/oauth/token/", {"grant_type": "authorization_code"})
        self.assertExceptionJson(request, ClientNotProvided())
        
        request = self.client.post("/oauth/token/", {"grant_type": "authorization_code", "client_id": ""})
        self.assertExceptionJson(request, ClientNotProvided())
        
        request = self.client.post("/oauth/token/", {"grant_type": "authorization_code", "client_id": 1234})
        self.assertExceptionJson(request, ClientDoesNotExist())
