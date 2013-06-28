from rest_framework import permissions


class TokenHasScope(permissions.BasePermission):

    def has_permission(self, request, view):
        from doac.decorators import scope_required

        scopes = getattr(view, "scopes", [])

        if not hasattr(request, "auth") or not request.auth:
            return False

        request.access_token = request.auth

        @scope_required(*scopes)
        def test_func(request):
            return "Pass"

        response = test_func(request)

        if response == "Pass":
            return True

        return False
