from django.test import TestCase
from oauth2_consumer.models import AuthorizationToken, Client, RefreshToken, Scope
from django.contrib.auth.models import User


class TestAuthorizationTokenModel(TestCase):

    def setUp(self):
        self.oclient = Client(name="Test Client", access_host="http://localhost/")
        self.oclient.save()
        
        self.scope = Scope(short_name="test", full_name="Test Scope", description="Scope for testing")
        self.scope.save()
        
        self.user = User(username="test", password="test", email="test@test.com")
        self.user.save()
        
        self.token = AuthorizationToken(client=self.oclient, user=self.user)
        self.token.save()
        
        self.token.scope = [self.scope]
        self.token.save()

    def test_unicode(self):
        self.assertEqual(unicode(self.token), self.token.token)
        
    def test_generate_refresh_token(self):
        rt = self.token.generate_refresh_token()
        
        self.assertEqual(RefreshToken.objects.count(), 1)
        self.assertIsInstance(rt, RefreshToken)
        
        rt = self.token.generate_refresh_token()
        
        self.assertEqual(RefreshToken.objects.count(), 1)
        self.assertIsNone(rt)
        
        self.token.is_active = True
        rt = self.token.generate_refresh_token()
        
        self.assertEqual(RefreshToken.objects.count(), 1)
        self.assertIsNone(rt)
