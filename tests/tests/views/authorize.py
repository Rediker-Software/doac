from oauth2_consumer.models import AuthorizationCode, Client, RedirectUri, Scope
from ..test_cases import AuthorizeTestCase
import urllib


class TestErrors(AuthorizeTestCase):
    
    def test_client_id(self):
        from oauth2_consumer.exceptions.invalid_request import ClientNotProvided
        from oauth2_consumer.exceptions.invalid_client import ClientDoesNotExist
        
        request = self.client.get("/oauth/authorize/")
        self.assertExceptionRendered(request, ClientNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=")
        self.assertExceptionRendered(request, ClientNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=1234")
        self.assertExceptionRendered(request, ClientDoesNotExist())
    
    def test_redirect_uri(self):
        from oauth2_consumer.exceptions.invalid_request import RedirectUriNotProvided, RedirectUriDoesNotValidate
        
        request = self.client.get("/oauth/authorize/?client_id=%s" % (self.oauth_client.id, ))
        self.assertExceptionRendered(request, RedirectUriNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=" % (self.oauth_client.id, ))
        self.assertExceptionRendered(request, RedirectUriNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=invalid" % (self.oauth_client.id, ))
        self.assertExceptionRendered(request, RedirectUriDoesNotValidate())
    
    def test_scope(self):
        from oauth2_consumer.exceptions.invalid_scope import ScopeNotProvided, ScopeNotValid
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s" % (self.oauth_client.id, self.redirect_uri.url, ))
        self.assertExceptionRedirect(request, ScopeNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=" % (self.oauth_client.id, self.redirect_uri.url, ))
        self.assertExceptionRedirect(request, ScopeNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=invalid" % (self.oauth_client.id, self.redirect_uri.url, ))
        self.assertExceptionRedirect(request, ScopeNotValid())
    
    def test_response_type(self):
        from oauth2_consumer.exceptions.invalid_request import ResponseTypeNotProvided
        from oauth2_consumer.exceptions.unsupported_response_type import ResponseTypeNotValid
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=%s" % (self.oauth_client.id, self.redirect_uri.url, self.scope.short_name, ))
        self.assertExceptionRedirect(request, ResponseTypeNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=%s&response_type=" % (self.oauth_client.id, self.redirect_uri.url, self.scope.short_name, ))
        self.assertExceptionRedirect(request, ResponseTypeNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=%s&response_type=invalid" % (self.oauth_client.id, self.redirect_uri.url, self.scope.short_name, ))
        self.assertExceptionRedirect(request, ResponseTypeNotValid())


class TestResponse(AuthorizeTestCase):
    
    def setUp(self):
        super(TestResponse, self).setUp()
        
        self.redirect_uri = RedirectUri(client=self.oauth_client, url="http://localhost/oauth/redirect_endpoint/")
        self.redirect_uri.save()
    
    def test_approval_form(self):
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=%s&response_type=token" % (self.oauth_client.id, self.redirect_uri.url, self.scope.short_name, ))
        
        self.assertTemplateUsed(request, "oauth2_consumer/authorize.html")
        
        self.assertEqual(request.context["authorization_code"], AuthorizationCode.objects.all()[0])
        self.assertEqual(request.context["client"], self.oauth_client)
        self.assertEqual(request.context["scopes"], [self.scope])
        self.assertEqual(request.context["state"], "o2cs")
        
        self.assertEqual(AuthorizationCode.objects.count(), 1)
        