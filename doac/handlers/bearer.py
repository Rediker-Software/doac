from ..exceptions.base import InvalidToken
from ..exceptions.invalid_request import CredentialsNotProvided
from ..models import AccessToken
from ..utils import request_error_header


class BearerHandler:

    def access_token(self, value, request):
        """
        Try to get the `AccessToken` associated with the provided token.

        *The provided value must pass `BearerHandler.validate()`*
        """

        if self.validate(value, request) is not None:
            return None
        
        access_token = AccessToken.objects.for_token(value)
        
        return access_token
    
    def authenticate(self, value, request):
        """
        Try to get a user associated with the provided token.

        *The provided value must pass `BearerHandler.validate()`*
        """

        if self.validate(value, request) is not None:
            return None
        
        access_token = AccessToken.objects.for_token(value)
        
        return access_token.user
    
    def validate(self, value, request):
        """
        Try to get the `AccessToken` associated with the given token.

        The return value is determined based n a few things:

        - If no token is provided (`value` is None), a 400 response will  be returned.
        - If an invalid token is provided, a 401 response will be returned.
        - If the token provided is valid, `None` will be returned.
        """

        from django.http import HttpResponseBadRequest
        from doac.http import HttpResponseUnauthorized
        
        if not value:
            response = HttpResponseBadRequest()
            response["WWW-Authenticate"] = request_error_header(CredentialsNotProvided)
            
            return response
        
        try:
            access_token = AccessToken.objects.for_token(value)
        except AccessToken.DoesNotExist:
            response = HttpResponseUnauthorized()
            response["WWW-Authenticate"] = request_error_header(InvalidToken)
            
            return response
        
        return None
