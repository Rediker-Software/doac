from .http import HttpResponseUnauthorized


class InvalidRequest(Exception):
    error = "invalid_request"
    http = HttpResponseUnauthorized


class ClientNotProvided(InvalidRequest):
    reason = "The client was malformed or invalid"


class ClientDoesNotExist(InvalidRequest):
    reason = "The client was malformed or invalid."

    
class InvalidScope(Exception):
    error = "invalid_scope"