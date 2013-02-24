from django.http import HttpResponse
from oauth2_consumer.decorators import scope_required

@scope_required
def no_args(request):
    return HttpResponse("success")
