from django.contrib import admin
from .models import AccessToken, AuthorizationToken, Client, RedirectUri, RefreshToken, Scope

admin.site.register(AccessToken)
admin.site.register(AuthorizationToken)
admin.site.register(Client)
admin.site.register(RedirectUri)
admin.site.register(RefreshToken)
admin.site.register(Scope)