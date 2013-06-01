from django.db import models
from django.db.models.query import QuerySet


class CustomManager(models.Manager):
    """
    Custom manager that adds functionality for the custom query set.
    """
    
    def __getattr__(self, name):
        """
        Forwards methods called on the manager to its query set.
        """
        
        return getattr(self.get_query_set(), name)


class AccessTokenManager(CustomManager):
    
    def get_query_set(self):
        return AccessTokenQuerySet(self.model)


class AccessTokenQuerySet(QuerySet):
    
    def for_token(self, token):
        return self.get(token=token)
    
    def is_active(self):
        return self.filter(is_active=True)
    
    def with_client(self, client):
        return self.filter(client=client.id)
    
    def with_refresh_token(self, refresh_token):
        return self.filter(refresh_token=refresh_token.id)
    
    def with_user(self, user):
        return self.filter(user=user.pk)


class AuthorizationCodeManager(CustomManager):
    
    def get_query_set(self):
        return AuthorizationCodeQuerySet(self.model)


class AuthorizationCodeQuerySet(QuerySet):
    
    def for_token(self, token):
        return self.get(token=token)
    
    def is_active(self):
        return self.filter(is_active=True)

    def with_expiration_before(self, date):
        return self.filter(expires_at__lt=date)
    
    def with_client(self, client):
        return self.filter(client=client.id)
    
    def with_user(self, user):
        return self.filter(user=user.pk)


class AuthorizationTokenManager(CustomManager):
    
    def get_query_set(self):
        return AuthorizationTokenQuerySet(self.model)


class AuthorizationTokenQuerySet(QuerySet):
    
    def for_token(self, token):
        return self.get(token=token)
    
    def is_active(self):
        return self.filter(is_active=True)
    
    def with_client(self, client):
        return self.filter(client=client.id)
    
    def with_user(self, user):
        return self.filter(user=user.pk)


class ClientManager(CustomManager):
    
    def get_query_set(self):
        return ClientQuerySet(self.model)


class ClientQuerySet(QuerySet):

    def for_id(self, id):
        return self.get(id=id)

    def for_secret(self, secret):
        return self.get(secret=secret)
    
    def is_active(self):
        return self.filter(is_active=True)


class RedirectUriManager(CustomManager):
    
    def get_query_set(self):
        return RedirectUriQuerySet(self.model)


class RedirectUriQuerySet(QuerySet):

    def for_url(self, url):
        return self.filter(url=url)

    def with_client(self, client):
        return self.filter(client=client.id)


class RefreshTokenManager(CustomManager):
    
    def get_query_set(self):
        return RefreshTokenQuerySet(self.model)


class RefreshTokenQuerySet(QuerySet):
    
    def for_token(self, token):
        return self.get(token=token)
    
    def is_active(self):
        return self.filter(is_active=True)
    
    def with_authorization_token(self, authorization_token):
        return self.filter(authorization_token=authorization_token.id)
    
    def with_client(self, client):
        return self.filter(client=client.id)
    
    def with_user(self, user):
        return self.filter(user=user.pk)


class ScopeManager(CustomManager):
    
    def get_query_set(self):
        return ScopeQuerySet(self.model)


class ScopeQuerySet(QuerySet):
    
    def for_short_name(self, name):
        return self.get(short_name=name)
