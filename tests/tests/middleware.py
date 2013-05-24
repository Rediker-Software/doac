from doac.middleware import AuthenticationMiddleware
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
        
        self.assertRaises(Exception, lambda _: AuthenticationMiddleware().process_request(request))
        
        #self.assertEqual(request.auth_type, "type")
    
    def test_invalid_bearer_token(self):
        request = self.factory.get("/")
        request.META["HTTP_AUTHORIZATION"] = "bearer invalid"
        
        self.assertRaises(Exception, lambda _: AuthenticationMiddleware().process_request(request))
        
        #self.assertEqual(request.auth_type, "bearer")
