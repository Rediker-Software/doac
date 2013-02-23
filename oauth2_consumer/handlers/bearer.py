from oauth2_consumer.models import AccessToken


class BearerHandler:

    def access_token(self, value, request):
        if not self.validate(value, request):
            return None
        
        access_token = AccessToken.objects.get(token=value)
        
        return access_token
    
    def authenticate(self, value, request):
        if not self.validate(value, request):
            return None
        
        access_token = AccessToken.objects.get(token=value)
        
        return access_token.user
    
    def validate(self, value, request):
        if not value:
            return False
        
        try:
            access_token = AccessToken.objects.get(token=value)
        except AccessToken.DoesNotExist:
            return False
        
        return True
