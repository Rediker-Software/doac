from django.test import TestCase
from oauth2_consumer.models import Client, RedirectUri

class TestErrors(TestCase):
    
    def setUp(self):
        self.oauth_client = Client(name="Test Client", access_host="http://localhost/")
        self.oauth_client.save()
        
        self.redirect_uri = RedirectUri(client=self.oauth_client, url="http://localhost/oauth/redirect_endpoint/")
        self.redirect_uri.save()
        
        self.client_secret = self.oauth_client.secret
    
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
        
        request = self.client.get("/oauth/authorize/?client_id=%s&request_uri=" % (self.oauth_client.id, ))
        self.assertEqual(request.content, "The redirect URI was malformed or invalid.")
        self.assertEqual(request.status_code, 401)
