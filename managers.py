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