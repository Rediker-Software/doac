from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .utils import total_seconds
from . import utils


ALLOWED_RESPONSE_TYPES = ("code", "token", )

ALLOWED_GRANT_TYPES = ("authorization_code", "refresh_token", )


class OAuthView(View):
    """
    All views must subclass this class.

    This provides common methods which are needed for validation and processing OAuth
    requests and responses.
    """

    def handle_exception(self, exception):
        """
        Handle a unspecified exception and return the correct method that should be used
        for handling it.

        If the exception has the `can_redirect` property set to False, it is
        rendered to the browser.  Otherwise, it will be redirected to the location
        provided in the `RedirectUri` object that is associated with the request.
        """

        can_redirect = getattr(exception, "can_redirect", True)
        redirect_uri = getattr(self, "redirect_uri", None)

        if can_redirect and redirect_uri:
            return self.redirect_exception(exception)
        else:
            return self.render_exception(exception)

    def redirect_exception(self, exception):
        """
        Build the query string for the exception and return a redirect to the
        redirect uri that was associated with the request.
        """

        from django.http import QueryDict, HttpResponseRedirect

        query = QueryDict("").copy()
        query["error"] = exception.error
        query["error_description"] = exception.reason
        query["state"] = self.state

        return HttpResponseRedirect(self.redirect_uri.url + "?" + query.urlencode())

    def render_exception(self, exception):
        """
        Return a 401 response with the body being the reason for the exception.
        """

        from .http import HttpResponseUnauthorized

        return HttpResponseUnauthorized(exception.reason)

    def render_exception_js(self, exception):
        """
        Return a response with the body containing a JSON-formatter version of the exception.
        """

        from .http import JsonResponse

        response = {}
        response["error"] = exception.error
        response["error_description"] = exception.reason

        return JsonResponse(response, status=getattr(exception, 'code', 400))

    def verify_dictionary(self, dict, *args):
        """
        Based on a provided `dict`, validate all of the contents of that dictionary that are
        provided.

        For each argument provided that isn't the dictionary, this will set the raw value of
        that key as the instance variable of the same name.  It will then call the verification
        function named `verify_[argument]` to verify the data.
        """

        for arg in args:
            setattr(self, arg, dict.get(arg, None))

            if hasattr(self, "verify_" + arg):
                func = getattr(self, "verify_" + arg)
                func()

    def verify_client_id(self):
        """
        Verify a provided client id against the database and set the `Client` object that is
        associated with it to `self.client`.

        TODO: Document all of the thrown exceptions.
        """

        from .models import Client
        from .exceptions.invalid_client import ClientDoesNotExist
        from .exceptions.invalid_request import ClientNotProvided

        if self.client_id:
            try:
                self.client = Client.objects.for_id(self.client_id)
            # Catching also ValueError for the case when client_id doesn't contain an integer.
            except (Client.DoesNotExist, ValueError):
                raise ClientDoesNotExist()
        else:
            raise ClientNotProvided()

    def verify_redirect_uri(self):
        from urlparse import urlparse
        from .models import RedirectUri
        from .exceptions.invalid_request import RedirectUriDoesNotValidate, RedirectUriNotProvided

        PARSE_MATCH_ATTRIBUTES = ("scheme", "hostname", "port", )

        if self.redirect_uri:
            client_host = self.client.access_host
            client_parse = urlparse(client_host)

            redirect_parse = urlparse(self.redirect_uri)

            for attribute in PARSE_MATCH_ATTRIBUTES:
                client_attribute = getattr(client_parse, attribute)
                redirect_attribute = getattr(redirect_parse, attribute)

                if not client_attribute == redirect_attribute:
                    raise RedirectUriDoesNotValidate()

            try:
                self.redirect_uri = RedirectUri.objects.with_client(self.client).for_url(self.redirect_uri)
            except RedirectUri.DoesNotExist:
                raise RedirectUriDoesNotValidate()
        else:
            raise RedirectUriNotProvided()


class ApprovalView(OAuthView):

    http_method_names = ("post", )

    def post(self, request, *args, **kwargs):
        utils.prune_old_authorization_codes()

        try:
            self.verify_dictionary(request.POST, "code")
        except Exception, e:
            return self.render_exception(e)

        self.client = self.authorization_code.client
        self.redirect_uri = self.authorization_code.redirect_uri
        self.scopes = self.authorization_code.scope.all()
        self.state = request.POST.get("code_state", None)

        if "deny_access" in request.POST:
            return self.authorization_denied()
        else:
            return self.authorization_accepted()

    def authorization_accepted(self):
        from django.http import HttpResponseRedirect
        from .models import AuthorizationToken

        self.authorization_token = AuthorizationToken(user=self.request.user, client=self.client)
        self.authorization_token.save()

        self.authorization_token.scope = self.scopes
        self.authorization_token.save()

        if self.authorization_code.response_type == "code":
            separator = "?"
        else:
            separator = "#"

            self.access_token = self.authorization_token.generate_refresh_token().generate_access_token()

        query_string = self.generate_query_string()

        return HttpResponseRedirect(self.redirect_uri.url + separator + query_string)

    def authorization_denied(self):
        from .exceptions.access_denied import AuthorizationDenied

        return self.redirect_exception(AuthorizationDenied())

    def generate_query_string(self):
        from django.http import QueryDict

        query = QueryDict("").copy()
        query["state"] = self.state

        if self.authorization_code.response_type == "token":
            query["access_token"] = self.access_token.token
        else:
            query["code"] = self.authorization_token.token

        return query.urlencode()

    def verify_code(self):
        from .models import AuthorizationCode
        from .exceptions.invalid_request import AuthorizationCodeNotValid, AuthorizationCodeNotProvided

        if self.code:
            get_code = self.request.GET.get("code", None)

            if not get_code == self.code:
                raise AuthorizationCodeNotValid()

            try:
                self.authorization_code = AuthorizationCode.objects.for_token(self.code)
            except AuthorizationCode.DoesNotExist:
                raise AuthorizationCodeNotValid()
        else:
            raise AuthorizationCodeNotProvided()


class AuthorizeView(OAuthView):

    http_method_names = ("get", "post", )

    def get(self, request, *args, **kwargs):
        from django.contrib.auth.views import redirect_to_login

        utils.prune_old_authorization_codes()

        self.state = request.GET.get("state", "o2cs")

        try:
            self.verify_dictionary(request.GET, "client_id", "redirect_uri", "scope", "response_type")
        except Exception, e:
            return self.handle_exception(e)

        if not request.user.is_active:
            return redirect_to_login(request.get_full_path())

        code = self.generate_authorization_code()

        context = {
            "authorization_code": code,
            "client": self.client,
            "oauth_title": "Request for Permission",
            "scopes": self.scopes,
            "state": self.state,
        }

        return TemplateResponse(request, "doac/authorize.html", context)

    def generate_authorization_code(self):
        from .models import AuthorizationCode

        code = AuthorizationCode(client=self.client, redirect_uri=self.redirect_uri, response_type=self.response_type)
        code.save()

        code.scope = self.scopes
        code.save()

        return code

    def verify_response_type(self):
        from .exceptions.unsupported_response_type import ResponseTypeNotValid
        from .exceptions.invalid_request import ResponseTypeNotProvided

        if self.response_type:
            if not self.response_type in ALLOWED_RESPONSE_TYPES:
                raise ResponseTypeNotValid()
        else:
            raise ResponseTypeNotProvided()

    def verify_scope(self):
        from .models import Scope
        from .exceptions.invalid_scope import ScopeNotProvided, ScopeNotValid

        if self.scope:
            scopes = self.scope.split(" ")
            self.scopes = []

            for scope_name in scopes:
                try:
                    scope = Scope.objects.for_short_name(scope_name)
                except Scope.DoesNotExist:
                    raise ScopeNotValid()

                self.scopes.append(scope)
        else:
            raise ScopeNotProvided()


class TokenView(OAuthView):

    http_method_names = ("post", )

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(TokenView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.verify_dictionary(request.POST, "grant_type", "client_id", "client_secret")
        except Exception, e:
            return self.render_exception_js(e)

        if self.grant_type == "authorization_code":
            try:
                self.verify_dictionary(request.POST, "code")
            except Exception, e:
                return self.render_exception_js(e)

            self.refresh_token = self.authorization_token.generate_refresh_token()

            if not self.refresh_token:
                self.authorization_token.revoke_tokens()

            self.access_token = self.refresh_token.generate_access_token()

            return self.render_authorization_token()

        elif self.grant_type == "refresh_token":
            try:
                self.verify_dictionary(request.POST, "refresh_token")
            except Exception, e:
                return self.render_exception_js(e)

            self.access_token = self.refresh_token.generate_access_token()

            return self.render_refresh_token()

    def render_authorization_token(self):
        from .compat import now
        from .http import JsonResponse

        remaining = self.refresh_token.expires_at - now()

        response = {}
        response["refresh_token"] = self.refresh_token.token
        response["token_type"] = "bearer"
        response["expires_in"] = int(total_seconds(remaining))
        response["access_token"] = self.access_token.token

        return JsonResponse(response)

    def render_refresh_token(self):
        from .compat import now
        from .http import JsonResponse

        remaining = self.access_token.expires_at - now()

        response = {}
        response["token_type"] = "bearer"
        response["expires_in"] = int(total_seconds(remaining))
        response["access_token"] = self.access_token.token

        return JsonResponse(response)

    def verify_client_secret(self):
        from .exceptions.invalid_client import ClientSecretNotValid
        from .exceptions.invalid_request import ClientSecretNotProvided

        if self.client_secret:
            if not self.client.secret == self.client_secret:
                raise ClientSecretNotValid()
        else:
            raise ClientSecretNotProvided()

    def verify_code(self):
        from .exceptions.invalid_request import AuthorizationCodeAlreadyUsed, AuthorizationCodeNotProvided, AuthorizationCodeNotValid
        from .models import AuthorizationToken

        if self.code:
            try:
                self.authorization_token = AuthorizationToken.objects.with_client(self.client).for_token(self.code)

                if not self.authorization_token.is_active:
                    self.authorization_token.revoke_tokens()

                    raise AuthorizationCodeAlreadyUsed()
            except AuthorizationToken.DoesNotExist:
                raise AuthorizationCodeNotValid()
        else:
            raise AuthorizationCodeNotProvided()

    def verify_grant_type(self):
        from .exceptions.unsupported_grant_type import GrantTypeNotProvided, GrantTypeNotValid

        self.grant_type = self.request.POST.get("grant_type", None)

        if self.grant_type:
            if not self.grant_type in ALLOWED_GRANT_TYPES:
                raise GrantTypeNotValid()
        else:
            raise GrantTypeNotProvided()

    def verify_refresh_token(self):
        from .exceptions.invalid_request import RefreshTokenNotProvided, RefreshTokenNotValid
        from .models import RefreshToken

        if self.refresh_token:
            try:
                self.refresh_token = RefreshToken.objects.with_client(self.client).for_token(self.refresh_token)
            except RefreshToken.DoesNotExist:
                raise RefreshTokenNotValid()
        else:
            raise RefreshTokenNotProvided()
