from oauth2_consumer.middleware import AuthenticationMiddleware
from .test_cases import MiddlewareTestCase


class TestMiddleware(MiddlewareTestCase):
    
    def test_no_token(self):
        request = self.factory.get("/")
        
        AuthenticationMiddleware().process_request(request)
        
        self.assertEqual(request.auth_type, None)
        self.assertFalse(hasattr(request, "acess_token"))
        self.assertFalse(hasattr(request, "user"))
    
    def test_invalid_handler(self):
        request = self.factory.get("/")
        request.META["HTTP_AUTHORIZATION"] = "type token"
        
        AuthenticationMiddleware().process_request(request)
        
        print request
        
        self.assertEqual(request.auth_type, "type")
