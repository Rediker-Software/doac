from django.test import TestCase
from oauth2_consumer.models import AuthorizationToken, Client, Scope


class TokenTestCase(TestCase):
    
    def setUp(self):
        from django.contrib.auth.models import User
        
        self.user = User.objects.create_user("test", "test@test.com", "test")
        
        self.oauth_client = Client(name="Test Client", access_host="http://localhost/")
        self.oauth_client.save()
        
        self.client_secret = self.oauth_client.secret
        
        self.scope = Scope(short_name="test", full_name="Test Scope", description="This is a test scope.")
        self.scope.save()
        
        self.authorization_token = AuthorizationToken(user=self.user, client=self.oauth_client)
        self.authorization_token.save()
        
        self.authorization_token.scope = [self.scope]
        self.authorization_token.save()
