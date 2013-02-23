from django.test import TestCase
from oauth2_consumer.models import AuthorizationCode, AuthorizationToken, Client, RedirectUri, Scope


class OAuthTestCase(TestCase):
    
    def setUp(self):
        from django.contrib.auth.models import User
        
        self.user = User.objects.create_user("test", "test@test.com", "test")
        
        self.oauth_client = Client(name="Test Client", access_host="http://localhost/")
        self.oauth_client.save()
        
        self.scope = Scope(short_name="test", full_name="Test Scope", description="This is a test scope.")
        self.scope.save()
    
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


class AuthorizeTestCase(OAuthTestCase):
    
    def setUp(self):
        super(AuthorizeTestCase, self).setUp()
        
        self.redirect_uri = RedirectUri(client=self.oauth_client, url="http://localhost/oauth/redirect_endpoint/")
        self.redirect_uri.save()


class TokenTestCase(OAuthTestCase):
    
    def setUp(self):
        super(TokenTestCase, self).setUp()
        
        self.client_secret = self.oauth_client.secret
        
        self.authorization_token = AuthorizationToken(user=self.user, client=self.oauth_client)
        self.authorization_token.save()
        
        self.authorization_token.scope = [self.scope]
        self.authorization_token.save()
