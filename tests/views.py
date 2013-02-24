from django.http import HttpResponse
from oauth2_consumer.decorators import scope_required

@scope_required()
def no_args(request):
    return HttpResponse("success")

@scope_required("test")
def has_scope(request):
    return HttpResponse("success")

@scope_required("invalid")
def scope_doesnt_exist(request):
    return HttpResponse("success")

@scope_required("test", "invalid")
def doesnt_have_all_scope(request):
    return HttpResponse("success")
