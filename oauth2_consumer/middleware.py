HANDLERS = ("oauth2_consumer.handlers.bearer.BearerHandler", )


class AuthenticationMiddleware:
    
    def process_request(self, request):
        self.request = request
        
        http_authorization = request.META.get("HTTP_AUTHORIZATION", None)
        
        request.auth_type = None
        
        if not http_authorization:
            return
        
        auth = http_authorization.split()
        
        self.auth_type = auth[0].lower()
        self.auth_value = " ".join(auth[1:]).strip()
        
        self.validate_auth_type()
        
        print "0"
        
        if not self.handler_name:
            return
        
        self.load_handler()
        
        print "1"
        
        if not self.handler:
            return
        
        if not self.handler.validate(self.auth_value):
            return
        
        print "Valid"
        
    def load_handler(self):
        if not self.handler_name:
            return
        
        handler_path = self.handler_name.split(".")
        
        handler_module = __import__(".".join(handler_path[:-1]), {}, {}, str(handler_path[-1]))
        self.handler = getattr(handler_module, handler_path[-1])()
    
    def validate_auth_type(self):
        for handler in HANDLERS:
            handler_type = handler.split(".")[-2]
            
            print handler_type
            
            if handler_type == self.auth_type:
                self.handler_name = handler
                
                return
        
        self.handler_name = None
