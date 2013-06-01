from django.core.urlresolvers import reverse
from rauth import OAuth2Service

from doac.models import AuthorizationToken
from ..test_cases import ApprovalTestCase


class TestRauth(ApprovalTestCase):
    
    def setUp(self):
        super(TestRauth, self).setUp()
        
        self.service = OAuth2Service(
            client_id=self.oauth_client.id,
            client_secret=self.oauth_client.secret,
            authorize_url=reverse("oauth2_authorize"),
        )
    
    def test_flow(self):
        self.client.login(username="test", password="test")
        
        authorization_url = self.service.get_authorize_url(**{
            "redirect_uri": self.redirect_uri.url,
            "response_type": "code",
            "scope": self.scope.short_name,
            "state": "test_state",
        })
        
        response = self.client.get(authorization_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doac/authorize.html")
        
        approval_url = reverse("oauth2_approval") + "?code=" + self.authorization_code.token
        
        response = self.client.post(approval_url, {
            "code": self.authorization_code.token,
            "code_state": "test_state",
            "approve_access": None,
        })
        
        authorization_token = AuthorizationToken.objects.all()[0]
