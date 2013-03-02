from django.utils.decorators import available_attrs
from functools import wraps
from oauth2_consumer.exceptions.invalid_request import CredentialsNotProvided
from oauth2_consumer.exceptions.insufficient_scope import ScopeNotEnough


def scope_required(*scopes):
    
    def decorator(view_func):
    
        wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            from django.http import HttpResponseForbidden
            from oauth2_consumer.models import Scope
            
            try:
                if not hasattr(request, "access_token"):
                    raise CredentialsNotProvided()
                
                access_token = request.access_token
                
                for scope_name in scopes:
                    try:
                        scope = access_token.scope.get(short_name=scope_name)
                    except Scope.DoesNotExist:
                        raise ScopeNotEnough()
            except:
                return HttpResponseForbidden("There was an error that prevented this request from continuing.")
            
            return view_func(request, *args, **kwargs)
            
        return _wrapped_view
    
    if scopes and hasattr(scopes[0], "__call__"):
        func = scopes[0]
        scopes = scopes[1:]
        return decorator(func)
    
    return decorator
