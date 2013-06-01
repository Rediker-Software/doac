from django.conf import settings
import datetime


class Settings:
    
    def __init__(self, options):
        self.handlers = options.get("HANDLERS", None)
        
        if not self.handlers:
            self.handlers = (
                "doac.handlers.bearer.BearerHandler",
            )
        
        self.realm = options.get("REALM", "oauth")
        
        self.access_token = options.get("ACCESS_TOKEN", {})
        self.setup_access_token()
        
        self.auth_code = options.get("AUTHORIZATION_CODE", {})
        self.setup_auth_code()
        
        self.auth_token = options.get("AUTHORIZATION_TOKEN", {})
        self.setup_auth_token()
        
        self.client = options.get("CLIENT", {})
        self.setup_client()
        
        self.refresh_token = options.get("REFRESH_TOKEN", {})
        self.setup_refresh_token()
        
    def setup_access_token(self):
        at = self.access_token
        token = {}
        
        token["expires"] = at.get("EXPIRES", datetime.timedelta(hours=2))
        token["length"] = at.get("LENGTH", 100)
        
        self.access_token = token
    
    def setup_auth_code(self):
        ac = self.auth_code
        token = {}
        
        token["expires"] = ac.get("EXPIRES", datetime.timedelta(minutes=15))
        token["length"] = ac.get("LENGTH", 100)
        
        self.auth_code = token
    
    def setup_auth_token(self):
        at = self.auth_token
        token = {}
        
        token["expires"] = at.get("EXPIRES", datetime.timedelta(minutes=15))
        token["length"] = at.get("LENGTH", 100)
        
        self.auth_token = token
    
    def setup_client(self):
        cli = self.client
        client = {}
        
        client["length"] = cli.get("LENGTH", 50)
        
        self.client = client
    
    def setup_refresh_token(self):
        rt = self.refresh_token
        token = {}
        
        token["expires"] = rt.get("EXPIRES", datetime.timedelta(days=60))
        token["length"] = rt.get("LENGTH", 100)
        
        self.refresh_token = token

options_dict = getattr(settings, "OAUTH_CONFIG", {})
options = Settings(options_dict)
