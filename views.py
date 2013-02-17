from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import View
from . import exceptions


ALLOWED_RESPONSE_TYPES = ("code", "token", )


class OAuthView(View):
    
    def check_get_parameters(self, *parameters):
        for parameter in parameters:
            if not self.request.GET.has_key(parameter):
                return False
        return True
    
    def redirect_exception(self, exception):
        from django.http import QueryDict
        
        query = QueryDict("").copy()
        query["error"] = exception.error
        query["error_description"] = exception.reason
        query["state"] = self.state
        
        return exception.http(self.redirect_uri.url + "?" + query.urlencode())
    
    def render_exception(self, exception):
        return exception.http(exception.reason)
    
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
        from .models import RedirectUri
            
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
            
            try:
                self.redirect_uri = RedirectUri.objects.get(client=self.client, url=self.redirect_uri)
            except RedirectUri.DoesNotExist:
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
        
        try:
            self.response_type = request.GET.get("response_type", None)
            self.verify_response_type()
        except (exceptions.InvalidRequest, exceptions.ResponseTypeNotValid) as e:
            return self.render_exception(e)
        
        self.state = request.GET.get("state", "o2cs")
        
        code = self.generate_authorization_code()
        
        context = {
            "authorization_code": code,
            "client": self.client,
            "oauth_title": "Request for Permission",
            "scopes": self.scopes,
            "state": self.state,
        }
        
        return TemplateResponse(request, "oauth2_consumer/authorize.html", context)
    
    
    def generate_authorization_code(self):
        from .models import AuthorizationCode
        
        code = AuthorizationCode(client=self.client, redirect_uri=self.redirect_uri)
        code.save()
        
        code.scope = self.scopes
        code.save()
        
        return code
    
    
    def verify_response_type(self):
        if self.response_type:
            if not self.response_type in ALLOWED_RESPONSE_TYPES:
                raise exceptions.ResponseTypeNotValid()
        else:
            raise exceptions.ResponseTypeNotDefined()
    
    
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
