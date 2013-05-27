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
