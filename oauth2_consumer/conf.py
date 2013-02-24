from django.conf import settings

class Settings:
    
    def __init__(self, options):
        self.handlers = options.get("HANDLERS", None)
        
        if not self.handlers:
            self.handlers = (
                "oauth2_consumer.handlers.bearer.BearerHandler",
            )

options_dict = getattr(settings, "OAUTH_CONFIG", {})
options = Settings(options_dict)
