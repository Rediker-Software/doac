from rest_framework import authentication, exceptions


class DoacAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        Send the request through the authentication middleware that
        is provided with DOAC and grab the user and token from it.
        """

        from doac.middleware import AuthenticationMiddleware

        try:
            response = AuthenticationMiddleware().process_request(request)
        except:
            raise exceptions.AuthenticationFailed("Invalid handler")

        if not hasattr(request, "user") or not request.user.is_authenticated():
            return None

        if not hasattr(request, "access_token"):
            raise exceptions.AuthenticationFailed("Access token was not valid")

        return request.user, request.access_token

    def authenticate_header(self, request):
        """
        DOAC specifies the realm as Bearer by default.
        """

        from doac.conf import options

        return 'Bearer realm="%s"' % options.realm
