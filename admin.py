from django.contrib import admin
from .models import AccessToken, AuthorizationCode, AuthorizationToken, Client, RedirectUri, RefreshToken, Scope


class AuthorizationCodeAdmin(admin.ModelAdmin):
    list_display = ("client", "redirect_uri", "token", )
    list_filter = ("created_at", "expires_at", "is_active", )


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "secret", "access_host", )
    list_filter = ("is_active", )


class RedirectUriAdmin(admin.ModelAdmin):
    list_display = ("client", "url", )


class ScopeAdmin(admin.ModelAdmin):
    list_display = ("short_name", "full_name", "description", )


admin.site.register(AccessToken)
admin.site.register(AuthorizationCode, AuthorizationCodeAdmin)
admin.site.register(AuthorizationToken)
admin.site.register(Client, ClientAdmin)
admin.site.register(RedirectUri, RedirectUriAdmin)
admin.site.register(RefreshToken)
admin.site.register(Scope, ScopeAdmin)
