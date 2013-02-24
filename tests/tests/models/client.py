from django.test import TestCase
from oauth2_consumer.models import Client


class TestClientModel(TestCase):
    
    def test_unicode(self):
        client = Client(name="Test Client", access_host="http://localhost/")
        client.save()
        
        self.assertEqual(unicode(client), client.name)
    
    def test_generate_secret(self):
        client = Client(name="Test Client", access_host="http://localhost/")
        secret = client.generate_secret()
        
        self.assertEqual(len(secret), 50)
