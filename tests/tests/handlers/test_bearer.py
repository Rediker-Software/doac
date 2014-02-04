from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from doac.handlers.bearer import BearerHandler
from doac.models import AuthorizationToken, Client, Scope
from doac.utils import request_error_header


class TestBearerHandler(TestCase):
    
    def setUp(self):
        self.oclient = Client(name="Test Client", access_host="http://localhost/")
        self.oclient.save()
        
        self.scope = Scope(short_name="test", full_name="Test Scope", description="Scope for testing")
        self.scope.save()
        
        self.user = User(username="Test", password="test", email="test@test.com")
        self.user.save()
        
        self.at = AuthorizationToken(client=self.oclient, user=self.user)
        self.at.save()
        self.at.scope = [self.scope]
        self.at.save()
        
        self.rt = self.at.generate_refresh_token()
        
        self.token = self.rt.generate_access_token()
        
        self.handler = BearerHandler()
        
        self.factory = RequestFactory()

    def test_access_token(self):
        request = self.factory.get("/")
        
        token = self.handler.access_token(self.token.token, request)
        
        self.assertEqual(token, self.token)
        
        token = self.handler.access_token("invalid", request)
        
        self.assertEqual(token, None)
    
    def test_authenticate(self):
        request = self.factory.get("/")
        
        user = self.handler.authenticate(self.token.token, request)
        
        self.assertEqual(user, self.user)
        
        user = self.handler.authenticate("invalid", request)
        
        self.assertEqual(user, None)
    
    def test_validate(self):
        from doac.exceptions.base import InvalidToken
        from doac.exceptions.invalid_request import CredentialsNotProvided
        
        request = self.factory.get("/")
        
        result = self.handler.validate(self.token.token, request)
        
        self.assertEqual(result, None)
        
        response = self.handler.validate("invalid", request)
        
        self.assertNotEqual(response, None)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["WWW-Authenticate"], request_error_header(InvalidToken))
        
        response = self.handler.validate("", request)
        
        self.assertNotEqual(response, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["WWW-Authenticate"], request_error_header(CredentialsNotProvided))
