from django.conf import settings
from django.db import models
from django.db.models import signals
from . import managers


class AccessToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="access_tokens")
    client = models.ForeignKey("Client", related_name="access_tokens")
    
    refresh_token = models.ForeignKey("RefreshToken", related_name="access_tokens")
    token = models.CharField(max_length=100)
    scope = models.ManyToManyField("Scope", related_name="access_tokens")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class AuthorizationCode(models.Model):
    client = models.ForeignKey("Client", related_name="authorization_codes")
    scope = models.ManyToManyField("Scope", related_name="authorization_codes")
    redirect_uri = models.ForeignKey("RedirectUri", related_name="authorization_codes")
    
    token = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.token
    
    def generate_token(self):
        from django.utils.crypto import get_random_string
        
        return get_random_string(100)
        
    def save(self, *args, **kwargs):
        from django.utils import timezone
        import datetime
        
        self.token = self.generate_token()
        self.expires_at = timezone.now() + datetime.timedelta(hours=1)
        
        super(AuthorizationCode, self).save(*args, **kwargs)


class AuthorizationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="authorization_tokens")
    client = models.ForeignKey("Client", related_name="authorization_tokens")
    token = models.CharField(max_length=100)
    scope = models.ManyToManyField("Scope", related_name="authorization_tokens")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.token
    
    def generate_refresh_token(self):
        if self.is_active:
            if not self.refresh_token:
                self.refresh_token = RefreshToken()
                
                self.refresh_token.client = self.client
                self.refresh_token.user = self.user
                self.refresh_token.save()
                
                self.refresh_token.scope = self.scope.all()
                self.refresh_token.save()
                
                self.is_active = False
                
                return self.refresh_token
            
        return None
    
    def generate_token(self):
        from django.utils.crypto import get_random_string
        
        return get_random_string(100)
        
    def save(self, *args, **kwargs):
        from django.utils import timezone
        import datetime
        
        self.token = self.generate_token()
        self.expires_at = timezone.now() + datetime.timedelta(hours=1)
        
        super(AuthorizationToken, self).save(*args, **kwargs)


class Client(models.Model):
    name = models.CharField(max_length=255)
    secret = models.CharField(max_length=50)
    access_host = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    def generate_secret(self):
        from django.utils.crypto import get_random_string
        
        return get_random_string(50)
        
    def save(self, *args, **kwargs):
        self.secret = self.generate_secret()
        
        super(Client, self).save(*args, **kwargs)


class RedirectUri(models.Model):
    client = models.ForeignKey("Client", related_name="redirect_uris")
    url = models.URLField(max_length=255)
    
    class Meta:
        verbose_name = "redirect URI"
    
    def __unicode__(self):
        return self.url


class RefreshToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="refresh_tokens")
    client = models.ForeignKey("Client", related_name="refresh_tokens")
    
    authorization_token = models.OneToOneField("AuthorizationToken", related_name="refresh_token")
    token = models.CharField(max_length=100)
    scope = models.ManyToManyField("Scope", related_name="refresh_tokens")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)


class Scope(models.Model):
    short_name = models.CharField(max_length=40)
    full_name = models.CharField(max_length=255)
    description = models.TextField()
