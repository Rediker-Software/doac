from django.core.urlresolvers import reverse
from django.http import HttpResponse
from oauth2_consumer.decorators import scope_required
from .test_cases import DecoratorTestCase
from .mock import TestFunc

class TestDecoratorErrors(DecoratorTestCase):
    def test_no_args(self):
        response = self.client.get(reverse("no_args"))
        
        self.assertEqual(response.status_code, 403)
        
        self.authorization_token.generate_refresh_token()
        self.authorization_token.refresh_token.generate_access_token()
        
        access_token = self.authorization_token.refresh_token.access_tokens.all()[0]
        
        response = self.client.get(reverse("no_args"), HTTP_AUTHORIZATION="Bearer %s" % (access_token.token, ))
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "success")
