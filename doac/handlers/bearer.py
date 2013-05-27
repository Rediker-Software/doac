from ..exceptions.base import InvalidToken
from ..exceptions.invalid_request import CredentialsNotProvided
from ..models import AccessToken
from ..utils import request_error_header


class BearerHandler:

    def access_token(self, value, request):
        if self.validate(value, request) is not None:
            return None
        
        access_token = AccessToken.objects.get(token=value)
        
        return access_token
    
    def authenticate(self, value, request):
        if self.validate(value, request) is not None:
            return None
        
        access_token = AccessToken.objects.get(token=value)
        
        return access_token.user
    
    def validate(self, value, request):
        from django.http import HttpResponseBadRequest
        from doac.http import HttpResponseUnauthorized
        
        if not value:
            response = HttpResponseBadRequest()
            response["WWW-Authenticate"] = request_error_header(CredentialsNotProvided)
            
            return response
        
        try:
            access_token = AccessToken.objects.get(token=value)
        except AccessToken.DoesNotExist:
            response = HttpResponseUnauthorized()
            response["WWW-Authenticate"] = request_error_header(InvalidToken)
            
            return response
        
        return None
