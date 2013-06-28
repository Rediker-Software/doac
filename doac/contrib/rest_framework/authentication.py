from rest_framework import authentication, exceptions


class DoacAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        Send the request through the authentication middleware that
        is provided with DOAC and grab the user and token from it.
        """

        from doac.middleware import AuthenticationMiddleware

        try:
            response = AuthenticationMiddleware().process_request(request._request)
        except:
            raise exceptions.AuthenticationFailed("Invalid handler")

        if not hasattr(request._request, "user") or not request._request.user.is_authenticated():
            raise exceptions.AuthenticationFailed("Could not authenticate")

        if not hasattr(request._request, "access_token"):
            raise exceptions.AuthenticationFailed("Access token was not valid")

        return request._request.user, request._request.access_token

    def authenticate_header(self, request):
        """
        DOAC specifies the realm as Bearer by default.
        """

        from doac.conf import options

        return 'Bearer realm="%s"' % options.realm
