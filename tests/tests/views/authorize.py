from django.test import TestCase
from oauth2_consumer.models import Client, RedirectUri
import urllib

class TestErrors(TestCase):
    
    def setUp(self):
        self.oauth_client = Client(name="Test Client", access_host="http://localhost/")
        self.oauth_client.save()
        
        self.redirect_uri = RedirectUri(client=self.oauth_client, url="http://localhost/oauth/redirect_endpoint/")
        self.redirect_uri.save()
        
        self.client_secret = self.oauth_client.secret
    
    def assertExceptionRendered(self, request, exception):
        
        self.assertEquals(request.content, exception.reason)
        self.assertEquals(request.status_code, 401)
    
    def assertExceptionRedirect(self, request, exception):
        params = {
            "error": exception.error,
            "error_description": exception.reason,
            "state": "o2cs",
        }
        
        url = self.redirect_uri.url + "?" + urllib.urlencode(params)
        
        self.assertRedirects(request, url)
        self.assertEquals(request.status_code, 302)
    
    def test_client_id(self):
        request = self.client.get("/oauth/authorize/")
        self.assertEqual(request.content, "The client was malformed or invalid.")
        self.assertEqual(request.status_code, 401)
        
        request = self.client.get("/oauth/authorize/?client_id=")
        self.assertEqual(request.content, "The client was malformed or invalid.")
        self.assertEqual(request.status_code, 401)
    
    def test_redirect_uri(self):
        request = self.client.get("/oauth/authorize/?client_id=%s" % (self.oauth_client.id, ))
        self.assertEqual(request.content, "The redirect URI was malformed or invalid.")
        self.assertEqual(request.status_code, 401)
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=" % (self.oauth_client.id, ))
        self.assertEqual(request.content, "The redirect URI was malformed or invalid.")
        self.assertEqual(request.status_code, 401)
    
    def test_scope(self):
        from oauth2_consumer.exceptions.invalid_scope import ScopeNotProvided, ScopeNotValid
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s" % (self.oauth_client.id, self.redirect_uri.url, ))
        self.assertExceptionRedirect(request, ScopeNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=" % (self.oauth_client.id, self.redirect_uri.url, ))
        self.assertExceptionRedirect(request, ScopeNotProvided())
        
        request = self.client.get("/oauth/authorize/?client_id=%s&redirect_uri=%s&scope=invalid" % (self.oauth_client.id, self.redirect_uri.url, ))
        self.assertExceptionRedirect(request, ScopeNotValid())
        