from django.http import HttpResponse
from oauth2_consumer.decorators import scope_required
from .test_cases import DecoratorTestCase
from .mock import TestFunc

class TestDecoratorErrors(DecoratorTestCase):
    def test_test(self):
        request = TestFunc()
        response = scope_required(request)
        
        self.assertFalse(request.called)
        
        @scope_required
        def view(request):
            return HttpResponse()
        
        request = self.factory.get("/")
        response = view(request)
        
        print response.status_code