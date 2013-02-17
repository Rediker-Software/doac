from .http import HttpResponseUnauthorized


class InvalidRequest(Exception):
    error = "invalid_request"
    http = HttpResponseUnauthorized


class ClientNotProvided(InvalidRequest):
    reason = "The client was malformed or invalid"


class ClientDoesNotExist(InvalidRequest):
    reason = "The client was malformed or invalid."


class RedirectUriNotProvided(InvalidRequest):
    reason = "The redirect URI was malformed or invalid."


class RedirectUriDoesNotValidate(InvalidRequest):
    reason = "The reidrect URI does not validate against the client host."


class InvalidScope(Exception):
    error = "invalid_scope"
    http = HttpResponseUnauthorized


class ScopeNotDefined(InvalidScope):
    reason = "The scope was malformed or invalid."


class ScopeNotValid(InvalidScope):
    reason = "The scope contained values which were incorrect."


class ResponseTypeNotDefined(InvalidRequest):
    reason = "The request type was malformed or invalid."


class ResponseTypeNotValid(Exception):
    error = "unsupported_response_type"
    http = HttpResponseUnauthorized
    reason = "The request type was malformed or invalid."


class AuthorizationCodeNotProvided(InvalidRequest):
    reason = "The authorization code was malformed or invalid."


class AuthorizationCodeNotValid(InvalidRequest):
    reason = "The authorization code was malformed or invalid."
