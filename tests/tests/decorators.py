from django.core.urlresolvers import reverse
from django.http import HttpResponse
from oauth2_consumer.decorators import scope_required
from .test_cases import DecoratorTestCase
from .mock import TestFunc

class TestDecoratorErrors(DecoratorTestCase):
    def test_no_args(self):
        response = self.client.get(reverse("no_args"))
        
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get(reverse("no_args"), HTTP_AUTHORIZATION="Bearer %s" % (self.access_token.token, ))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
    
    def test_scope_doesnt_exist(self):
        response = self.client.get(reverse("scope_doesnt_exist"))
        
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get(reverse("scope_doesnt_exist"), HTTP_AUTHORIZATION="Bearer %s" % (self.access_token.token, ))
        
        self.assertEqual(response.status_code, 403)
