from django.core.urlresolvers import reverse
from oauthlib.oauth2 import WebApplicationClient

from doac.models import AuthorizationToken
from ..test_cases import ApprovalTestCase


class TestOauthlib(ApprovalTestCase):
    
    def setUp(self):
        super(TestOauthlib, self).setUp()
        
        self.libclient = WebApplicationClient(self.oauth_client.id)
    
    def test_flow(self):
        self.client.login(username="test", password="test")
        
        request_uri = self.libclient.prepare_request_uri(
            "https://localhost" + reverse("oauth2_authorize"),
            redirect_uri=self.redirect_uri.url,
            scope=["test", ],
            state="test_state",
        )
        
        response = self.client.get(request_uri[17:])
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "oauth2_consumer/authorize.html")
        
        approval_url = reverse("oauth2_approval") + "?code=" + self.authorization_code.token
        
        response = self.client.post(approval_url, {
            "code": self.authorization_code.token,
            "code_state": "test_state",
            "approve_access": None,
        })
        
        authorization_token = AuthorizationToken.objects.all()[0]
