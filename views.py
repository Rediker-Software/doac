from django.http import HttpResponse


def redirect_endpoint(request):
    return HttpResponse(repr(dict(request.GET)))