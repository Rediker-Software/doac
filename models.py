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
    expires_at = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)


class AuthorizationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="authorization_tokens")
    client = models.ForeignKey("Client", related_name="authorization_tokens")
    token = models.CharField(max_length=100)
    scope = models.ManyToManyField("Scope", related_name="authorization_tokens")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)


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


class RefreshToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="refresh_tokens")
    client = models.ForeignKey("Client", related_name="refresh_tokens")
    
    authorization_token = models.OneToOneField("AuthorizationToken", related_name="refresh_token")
    token = models.CharField(max_length=100)
    scope = models.ManyToManyField("Scope", related_name="refresh_tokens")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)


class Scope(models.Model):
    short_name = models.CharField(max_length=40)
    full_name = models.CharField(max_length=255)
    description = models.TextField()
