def prune_old_authorization_codes():
    from .compat import now
    from .models import AuthorizationCode
    
    AuthorizationCode.objects.filter(expires_at__lt=now()).delete()


def get_handler(handler_name):
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
    from .conf import options
    
    header = "Bearer realm=\"%s\"" % (options.realm, )
    
    if hasattr(exception, "error"):
        header = header + ", error=\"%s\"" % (exception.error, )
    
    return header


def total_seconds(delta):
    return delta.days * 86400 + delta.seconds
