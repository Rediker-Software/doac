def prune_old_authorization_codes():
    from django.utils import timezone
    from .models import AuthorizationCode
    
    AuthorizationCode.objects.filter(expires_at__lt=timezone.now()).delete()