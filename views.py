from django.http import HttpResponse
from django.views.generic import View
from . import exceptions


class OAuthView(View):
    
    def check_get_parameters(self, *parameters):
        for parameter in parameters:
            if not self.request.GET.has_key(parameter):
                return False
        return True
    
    def render_exception(self, exception):
        return exception.http(exception.reason)
    
    def redirect_exception(self, exeption):
        pass
    
    def verify_client(self):
        from .models import Client
        
        if self.client_id:
            try:
                self.client = Client.objects.get(id=self.client_id)
            except Client.DoesNotExist:
                raise exceptions.ClientDoesNotExist()
        else:
            raise exceptions.ClientNotProvided()
        
    def verify_uri(self):
        from urlparse import urlparse
            
        PARSE_MATCH_ATTRIBUTES = ("scheme", "hostname", "port", )
        
        if self.redirect_uri:
            client_host = self.client.access_host
            client_parse = urlparse(client_host)
            
            redirect_parse = urlparse(self.redirect_uri)
            
            for attribute in PARSE_MATCH_ATTRIBUTES:
                client_attribute = getattr(client_parse, attribute)
                redirect_attribute = getattr(redirect_parse, attribute)
                
                if not client_attribute == redirect_attribute:
                    raise exceptions.RedirectUriDoesNotValidate()
        else:
            raise exceptions.RedirectUriNotProvided()


class AuthorizeView(OAuthView):
    
    http_method_names = ("get", "post", )
    
    def get(self, request, *args, **kwargs):
        try:
            self.client_id = request.GET.get("client_id", None)
            self.verify_client()
        except exceptions.InvalidRequest as e:
            return self.render_exception(e)
        
        try:
            self.redirect_uri = request.GET.get("redirect_uri", None)
            self.verify_uri()
        except exceptions.InvalidRequest as e:
            return self.render_exception(e)
        
        try:
            self.scope = request.GET.get("scope", None)
            self.verify_scope()
        except exceptions.InvalidScope as e:
            return self.render_exception(e)
    
    def verify_scope(self):
        from .models import Scope
        
        if self.scope:
            scopes = self.scope.split(",")
            self.scopes = []
            
            for scope_name in scopes:
                try:
                    scope = Scope.objects.get(short_name=scope_name)
                except Scope.DoesNotExist:
                    raise exceptions.ScopeNotValid()
                
                self.scopes.append(scope)
        else:
            raise exceptions.ScopeNotDefined()


def redirect_endpoint(request):
    return HttpResponse(repr(dict(request.GET)))
