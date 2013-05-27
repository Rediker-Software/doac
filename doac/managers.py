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
    
    def is_active(self):
        return self.filter(active=True)


class AuthorizationCodeManager(CustomManager):
    
    def get_query_set(self):
        return AuthorizationCodeQuerySet(self.model)


class AuthorizationCodeQuerySet(QuerySet):
    pass


class AuthorizationTokenManager(CustomManager):
    pass


class AuthorizationTokenQuerySet(QuerySet):
    pass


class ClientManager(CustomManager):
    pass


class ClientQuerySet(QuerySet):
    pass


class RedirectUriManager(CustomManager):
    pass


class RedirectUriQuerySet(QuerySet):
    pass


class RefreshTokenManager(CustomManager):
    pass


class RefreshTokenQuerySet(QuerySet):
    pass


class ScopeManager(CustomManager):
    pass


class ScopeQuerySet(QuerySet):
    pass
