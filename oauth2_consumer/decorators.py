from django.utils.decorators import available_attrs
from functools import wraps


def scope_required(*scopes):
    
    def decorator(view_func):
    
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            access_token = request.access_token
            
            for scope_name in scopes:
                try:
                    scope = access_token.scope.get(short_name=scope_name)
                except Scope.DoesNotExist:
                    raise
            
            return view_func(request, *args, **kwargs)
            
        return _wrapped_view
    
    return decorator
