from django.core.urlresolvers import reverse
from ..test_cases import ApprovalTestCase


class TestApprovalErrors(ApprovalTestCase):
    
    def test_code(self):
        from oauth2_consumer.exceptions.invalid_request import AuthorizationCodeNotValid, AuthorizationCodeNotProvided
        
        data = {
            "code": "invalid",
        }
        
        request = self.client.post(reverse("oauth2_approval") + "?code=%s" % (self.authorization_code.token, ), data)
        self.assertExceptionRendered(request, AuthorizationCodeNotValid())
