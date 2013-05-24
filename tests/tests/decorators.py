from django.core.urlresolvers import reverse
from django.http import HttpResponse
from doac.decorators import scope_required
from .test_cases import DecoratorTestCase


class TestDecoratorErrors(DecoratorTestCase):

    def test_no_args(self):
        @scope_required
        def no_args(request):
            return HttpResponse("success")
            
        response = no_args(self.request)
        
        self.assertEqual(response.status_code, 403)
        
        request = self.request
        request.META["HTTP_AUTHORIZATION"] = "Bearer %s" % (self.access_token.token, )
        self.mw.process_request(request)
        
        response = no_args(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")

    def test_no_args_with_parens(self):
        @scope_required()
        def no_args(request):
            return HttpResponse("success")
            
        response = no_args(self.request)
        
        self.assertEqual(response.status_code, 403)
        
        request = self.request
        request.META["HTTP_AUTHORIZATION"] = "Bearer %s" % (self.access_token.token, )
        self.mw.process_request(request)
        
        response = no_args(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
    
    def test_has_scope(self):
        @scope_required("test")
        def has_scope(request):
            return HttpResponse("success")
        
        response = has_scope(self.request)
        
        self.assertEqual(response.status_code, 403)
        
        request = self.request
        request.META["HTTP_AUTHORIZATION"] = "Bearer %s" % (self.access_token.token, )
        self.mw.process_request(request)
        
        response = has_scope(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
    
    def test_scope_doesnt_exist(self):
        @scope_required("invalid")
        def scope_doesnt_exist(request):
            return HttpResponse("success")
        
        response = scope_doesnt_exist(self.request)
        
        self.assertEqual(response.status_code, 403)
        
        request = self.request
        request.META["HTTP_AUTHORIZATION"] = "Bearer %s" % (self.access_token.token, )
        self.mw.process_request(request)
        
        response = scope_doesnt_exist(request)
        
        self.assertEqual(response.status_code, 403)
    
    def test_doesnt_have_all_scope(self):
        @scope_required("test", "invalid")
        def doesnt_have_all_scope(request):
            return HttpResponse("success")
        
        response = doesnt_have_all_scope(self.request)
        
        self.assertEqual(response.status_code, 403)
        
        request = self.request
        request.META["HTTP_AUTHORIZATION"] = "Bearer %s" % (self.access_token.token, )
        self.mw.process_request(request)
        
        response = doesnt_have_all_scope(self.request)
        
        self.assertEqual(response.status_code, 403)
