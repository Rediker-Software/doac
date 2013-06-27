from rest_framework import authentication


class DoacAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        Send the request through the authentication middleware that
        is provided with DOAC and grab the user and token from it.
        """

        from doac.middleware import AuthenticationMiddleware

        AuthenticationMiddleware().process_request(request._request)

        return request._request.user, request._request.access_token

    def authenticate_header(self, request):
        """
        DOAC specifies the realm as Bearer by default.
        """

        return 'Bearer realm="%s"' % self.www_authenticate_realm
