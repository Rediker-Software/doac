from django.core.urlresolvers import reverse
from django.http import HttpResponse
from oauth2_consumer.decorators import scope_required
from .test_cases import DecoratorTestCase


class TestDecoratorErrors(DecoratorTestCase):

    def test_no_args(self):
        @scope_required
        def no_args(request):
            return HttpResponse("success")
            
        response = no_args(self.request)
        
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get(reverse("no_args"), HTTP_AUTHORIZATION="Bearer %s" % (self.access_token.token, ))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
    
    def test_has_scope(self):
        response = self.client.get(reverse("has_scope"))
        
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get(reverse("has_scope"), HTTP_AUTHORIZATION="Bearer %s" % (self.access_token.token, ))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
    
    def test_scope_doesnt_exist(self):
        response = self.client.get(reverse("scope_doesnt_exist"))
        
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get(reverse("scope_doesnt_exist"), HTTP_AUTHORIZATION="Bearer %s" % (self.access_token.token, ))
        
        self.assertEqual(response.status_code, 403)
    
    def test_doesnt_have_all_scope(self):
        response = self.client.get(reverse("doesnt_have_all_scope"))
        
        self.assertEqual(response.status_code, 403)
        
        response = self.client.get(reverse("doesnt_have_all_scope"), HTTP_AUTHORIZATION="Bearer %s" % (self.access_token.token, ))
        
        self.assertEqual(response.status_code, 403)
