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
