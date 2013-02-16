from django.contrib import admin
from .models import AccessToken, AuthorizationToken, Client, RedirectUri, RefreshToken, Scope


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "secret", "access_host", )
    list_filter = ("is_active", )


class RedirectUriAdmin(admin.ModelAdmin):
    list_display = ("client", "url", )


admin.site.register(AccessToken)
admin.site.register(AuthorizationToken)
admin.site.register(Client, ClientAdmin)
admin.site.register(RedirectUri, RedirectUriAdmin)
admin.site.register(RefreshToken)
admin.site.register(Scope)