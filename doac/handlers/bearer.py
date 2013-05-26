from ..models import AccessToken


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
            return HttpResponseBadRequest()
        
        try:
            access_token = AccessToken.objects.get(token=value)
        except AccessToken.DoesNotExist:
            return HttpResponseUnauthorized()
        
        return None
