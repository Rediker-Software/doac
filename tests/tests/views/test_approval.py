from django.core.urlresolvers import reverse
from ..test_cases import ApprovalTestCase


class TestApprovalErrors(ApprovalTestCase):
    
    def test_code(self):
        from doac.exceptions.invalid_request import AuthorizationCodeNotValid, AuthorizationCodeNotProvided
        
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


class TestApprovalResponse(ApprovalTestCase):
    
    def test_denied(self):
        from doac.exceptions.access_denied import AuthorizationDenied
        
        data = {
            "code": self.authorization_code.token,
            "code_state": "o2cs",
            "deny_access": None,
        }
        
        request = self.client.post(reverse("oauth2_approval") + "?code=%s" % (self.authorization_code.token, ), data)
        self.assertExceptionRedirect(request, AuthorizationDenied())
    
    def test_approved_code(self):
        from doac.models import AuthorizationToken
        import urllib
        
        self.client.login(username="test", password="test")
        
        data = {
            "code": self.authorization_code.token,
            "code_state": "o2cs",
            "approve_access": None,
        }
        
        self.authorization_code.response_type = "code"
        self.authorization_code.save()
        
        request = self.client.post(reverse("oauth2_approval") + "?code=%s" % (self.authorization_code.token, ), data)
        self.assertEqual(request.status_code, 302)
        
        args = {
            "state": "o2cs",
            "code": AuthorizationToken.objects.all()[0].token,
        }
        self.assertRedirects(request, self.redirect_uri.url + "?" + urllib.urlencode(args))
    
    def test_approved_token(self):
        from doac.models import AccessToken
        import urllib
        
        self.client.login(username="test", password="test")
        
        data = {
            "code": self.authorization_code.token,
            "code_state": "o2cs",
            "approve_access": None,
        }
        
        self.authorization_code.response_type = "token"
        self.authorization_code.save()
        
        request = self.client.post(reverse("oauth2_approval") + "?code=%s" % (self.authorization_code.token, ), data)
        self.assertEqual(request.status_code, 302)
        
        args = {
            "state": "o2cs",
            "access_token": AccessToken.objects.all()[0].token,
        }
        self.assertRedirects(request, self.redirect_uri.url + "#" + urllib.urlencode(args))
