from django.core.urlresolvers import reverse
from ..test_cases import ApprovalTestCase


class TestApprovalErrors(ApprovalTestCase):
    
    def test_code(self):
        from oauth2_consumer.exceptions.invalid_request import AuthorizationCodeNotValid, AuthorizationCodeNotProvided
        
        request = self.client.post(reverse("oauth2_approval"))
        self.assertExceptionRendered(request, AuthorizationCodeNotProvided())
        
        request = self.client.post(reverse("oauth2_approval") + "?code=invalid")
        self.assertExceptionRendered(request, AuthorizationCodeNotProvided())
        
        request = self.client.post(reverse("oauth2_approval"), {"code": "invalid"})
        self.assertExceptionRendered(request, AuthorizationCodeNotValid())
        
        data = {
            "code": "invalid",
        }
        
        request = self.client.post(reverse("oauth2_approval") + "?code=%s" % (self.authorization_code.token, ), data)
        self.assertExceptionRendered(request, AuthorizationCodeNotValid())
        
        data = {
            "code": self.authorization_code.token,
        }
        
        request = self.client.post(reverse("oauth2_approval") + "?code=invalid", data)
        self.assertExceptionRendered(request, AuthorizationCodeNotValid())
        
        request = self.client.post(reverse("oauth2_approval") + "?code=invalid", {"code": "invalid"})
        self.assertExceptionRendered(request, AuthorizationCodeNotValid())
