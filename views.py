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
        from urlparse import urlsplit
        
        pass


class AuthorizeView(OAuthView):
    
    http_method_names = ("get", "post", )
    
    def get(self, request, *args, **kwargs):
        try:
            self.client_id = request.GET.get("client_id", None)
            self.verify_client()
        except exceptions.InvalidRequest as e:
            return self.render_exception(e)
        
        if self.check_get_parameters("client_id", "redirect_uri", "scope", "response_type"):
            return HttpResponse()
        else:
            if request.GET.has_key(""):
                pass


def redirect_endpoint(request):
    return HttpResponse(repr(dict(request.GET)))