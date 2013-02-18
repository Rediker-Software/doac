from django.contrib import admin
from .models import AccessToken, AuthorizationCode, AuthorizationToken, Client, RedirectUri, RefreshToken, Scope


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ("client", "user", "truncated_refresh_token", "truncated_token", )
    list_filter = ("created_at", "expires_at", "is_active", )
    
    def truncated_refresh_token(self, obj):
        return obj.refresh_token.token[0:40] + "..."
    truncated_refresh_token.short_description = "refresh token"
        
    def truncated_token(self, obj):
        return obj.token[0:40] + "..."
    truncated_token.short_description = "token"


class AuthorizationCodeAdmin(admin.ModelAdmin):
    list_display = ("client", "redirect_uri", "truncated_token", )
    list_filter = ("created_at", "expires_at", "is_active", )
        
    def truncated_token(self, obj):
        return obj.token[0:50] + "..."
    truncated_token.short_description = "token"


class AuthorizationTokenAdmin(admin.ModelAdmin):
    list_display = ("client", "user", "truncated_token")
    list_filter = ("created_at", "expires_at", "is_active", )
        
    def truncated_token(self, obj):
        return obj.token[0:75] + "..."
    truncated_token.short_description = "token"


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "secret", "access_host", )
    list_filter = ("is_active", )


class RedirectUriAdmin(admin.ModelAdmin):
    list_display = ("client", "url", )


class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ("client", "user", "truncated_authorization_token", "truncated_token", )
    list_filter = ("created_at", "expires_at", "is_active", )
        
    def truncated_authorization_token(self, obj):
        return obj.authorization_token.token[0:40] + "..."
    truncated_authorization_token.short_description = "token"
        
    def truncated_token(self, obj):
        return obj.token[0:40] + "..."
    truncated_token.short_description = "token"


class ScopeAdmin(admin.ModelAdmin):
    list_display = ("short_name", "full_name", "description", )


admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(AuthorizationCode, AuthorizationCodeAdmin)
admin.site.register(AuthorizationToken, AuthorizationTokenAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(RedirectUri, RedirectUriAdmin)
admin.site.register(RefreshToken, RefreshTokenAdmin)
admin.site.register(Scope, ScopeAdmin)
