def prune_old_authorization_codes():
    """
    Removes all unused and expired authorization codes from the database.
    """

    from .compat import now
    from .models import AuthorizationCode
    
    AuthorizationCode.objects.with_expiration_before(now()).delete()


def get_handler(handler_name):
    """
    Imports the module for a DOAC handler based on the string representation of the module path that is provided.
    """

    from .conf import options
    
    handlers = options.handlers
    
    for handler in handlers:
        handler_path = handler.split(".")
        name = handler_path[-2]
        
        if handler_name == name:
            handler_module = __import__(".".join(handler_path[:-1]), {}, {}, str(handler_path[-1]))
            
            return getattr(handler_module, handler_path[-1])()
    
    return None


def request_error_header(exception):
    """
    Generates the error header for a request using a Bearer token based on a given OAuth exception.
    """

    from .conf import options
    
    header = "Bearer realm=\"%s\"" % (options.realm, )
    
    if hasattr(exception, "error"):
        header = header + ", error=\"%s\"" % (exception.error, )
    
    if hasattr(exception, "reason"):
        header = header + ", error_description=\"%s\"" % (exception.reason, )
    
    return header


def total_seconds(delta):
    """
    Get the total seconds that a `datetime.timedelta` object covers.  Used for returning the total
    time until a token expires during the handshake process.
    """

    return delta.days * 86400 + delta.seconds
