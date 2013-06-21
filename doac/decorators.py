from django.utils.decorators import available_attrs
from functools import wraps
from .exceptions.invalid_request import CredentialsNotProvided
from .exceptions.insufficient_scope import ScopeNotEnough


def scope_required(*scopes):
    """
    Test for specific scopes that the access token has been authenticated for before
    processing the request and eventual response.

    The scopes that are passed in determine how the decorator will respond to incoming
    requests:

    - If no scopes are passed in the arguments, the decorator will test for any available
      scopes and determine the response based on that.

    - If specific scopes are passed, the access token will be checked to make sure it has
      all of the scopes that were requested.

    This decorator will change the response if the access toke does not have the scope:

    - If an invalid scope is requested (one that does not exist), all requests will be
      denied, as no access tokens will be able to fulfill the scope request and the
      request will be denied.

    - If the access token does not have one of the requested scopes, the request will be
      denied and the user will be returned one of two responses:

      - A 400 response (Bad Request) will be returned if an unauthenticated user tries to
        access the resource.

      - A 403 response (Forbidden) will be returned if an authenticated user ties to access
        the resource but does not have the correct scope.
    """
    
    def decorator(view_func):
    
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            from django.http import HttpResponseBadRequest, HttpResponseForbidden
            from .exceptions.base import InvalidRequest, InsufficientScope
            from .models import Scope
            from .utils import request_error_header
            
            try:
                if not hasattr(request, "access_token"):
                    raise CredentialsNotProvided()
                
                access_token = request.access_token
                
                for scope_name in scopes:
                    try:
                        scope = access_token.scope.for_short_name(scope_name)
                    except Scope.DoesNotExist:
                        raise ScopeNotEnough()
            except InvalidRequest as e:
                response = HttpResponseBadRequest()
                response["WWW-Authenticate"] = request_error_header(e)
            
                return response
            except InsufficientScope as e:
                response = HttpResponseForbidden()
                response["WWW-Authenticate"] = request_error_header(e)
                
                return response
            
            return view_func(request, *args, **kwargs)
            
        return _wrapped_view
    
    if scopes and hasattr(scopes[0], "__call__"):
        func = scopes[0]
        scopes = scopes[1:]
        return decorator(func)
    
    return decorator
