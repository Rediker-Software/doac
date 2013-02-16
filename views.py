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
        pass
    
    def redirect_exception(self, exeption):
        pass


class AuthorizeView(OAuthView):
    
    http_method_names = ("get", "post", )
    
    def get(self, request, *args, **kwargs):
    
        if self.check_get_parameters("client_id", "redirect_uri", "scope", "response_type"):
            return HttpResponse()
        else:
            return HttpResponse("Error")


def redirect_endpoint(request):
    return HttpResponse(repr(dict(request.GET)))