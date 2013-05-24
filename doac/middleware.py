

HANDLERS = ("doac.handlers.bearer.BearerHandler", )


class AuthenticationMiddleware:
    
    def process_request(self, request):
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
        
        if not self.handler.validate(self.auth_value, request):
            raise Exception("The authentication token could not be validated.")
        
        request.access_token = self.handler.access_token(self.auth_value, request)
        request.user = self.handler.authenticate(self.auth_value, request)
        
    def load_handler(self):
        handler_path = self.handler_name.split(".")
        
        handler_module = __import__(".".join(handler_path[:-1]), {}, {}, str(handler_path[-1]))
        self.handler = getattr(handler_module, handler_path[-1])()
    
    def validate_auth_type(self):
        for handler in HANDLERS:
            handler_type = handler.split(".")[-2]
            
            if handler_type == self.auth_type:
                self.handler_name = handler
                
                return
        
        self.handler_name = None
