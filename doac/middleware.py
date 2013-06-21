

HANDLERS = ("doac.handlers.bearer.BearerHandler", )


class AuthenticationMiddleware:
    
    def process_request(self, request):
        """
        Try to authenticate the user based on any given tokens that have been provided
        to the request object.  This will try to detect the authentication type and assign
        the detected User object to the `request.user` variable, similar to the standard
        Django authentication.
        """

        request.auth_type = None
        
        http_authorization = request.META.get("HTTP_AUTHORIZATION", None)
        
        if not http_authorization:
            return
        
        auth = http_authorization.split()
        
        self.auth_type = auth[0].lower()
        self.auth_value = " ".join(auth[1:]).strip()
        
        request.auth_type = self.auth_type
        
        self.validate_auth_type()
        
        if not self.handler_name:
            raise Exception("There is no handler defined for this authentication type.")
        
        self.load_handler()
        
        response = self.handler.validate(self.auth_value, request)
        
        if response is not None:
            return response
        
        request.access_token = self.handler.access_token(self.auth_value, request)
        request.user = self.handler.authenticate(self.auth_value, request)
        
    def load_handler(self):
        """
        Load the detected handler.
        """

        handler_path = self.handler_name.split(".")
        
        handler_module = __import__(".".join(handler_path[:-1]), {}, {}, str(handler_path[-1]))
        self.handler = getattr(handler_module, handler_path[-1])()
    
    def validate_auth_type(self):
        """
        Validate the detected authorization type against the list of handlers.  This will return the full
        module path to the detected handler.
        """

        for handler in HANDLERS:
            handler_type = handler.split(".")[-2]
            
            if handler_type == self.auth_type:
                self.handler_name = handler
                
                return
        
        self.handler_name = None
