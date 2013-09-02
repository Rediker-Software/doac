Integrating DOAC with other applications
========================================
DOAC should be compatible with any application that requires the default Django authentication.  But in some cases this is too broad, or you just need finer control over how it all works.

Django Rest Framework
----------------------
DOAC supports both authentication and permissions checking through Django Rest Framework.  This allows you to restrict authentication through access tokens to just the parts of your site which require it.

### Requirements

In order to use DOAC with Django Rest Framework, you must install them both first.

> pip install doac djangorestframework

### Integrating the authentication

You can use the authentication on a per-view basis or on a global level, DOAC works fine wherever you define the authentication for your API.

Globally, through the settings:
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'doac.contrib.rest_framework.authentication.DoacAuthentication',
    ),
}
```

Locally, using the API:
```
from rest_framework import viewsets
from doac.contrib.rest_framework import authentication

class ExampleViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.DoacAuthentication]
    model = ExampleModel
```

### Integrating the permissions

OAuth2 uses scopes to define what an access token can do with an application.  DOAC allows you to specify what scopes are allowed for accessing a viewset.

```
from rest_framework import viewsets
from doac.contrib.rest_framework import authentication, permissions

class ExampleViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.DoacAuthentication]
    permissions_classes = [permissions.TokenHasScope]
    model = ExampleModel
    
    scopes = ["read", "write", "fun_stuff"]
```

The scopes are checked in the same way as the `scope_required` decorator.  If no scopes are specified, all access tokens which have a scope are allowed access.  Any and all scopes specified will be checked in order to access the view, and any missing scopes will result in the access token being denied.

Insert application name here
----------------------------
Do you have an application that DOAC integrates with?  We are accepting [pull requests](https://github.com/Rediker-Software/doac) to the documentation, which means you can add your information here.