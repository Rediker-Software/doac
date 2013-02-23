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
