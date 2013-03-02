class AccessDenied(Exception):
    error = "access_denied"


class InsufficientScope(Exception):
    error = "insufficient_scope"


class InvalidClient(Exception):
    error = "invalid_client"


class InvalidGrant(Exception):
    error = "invalid_grant"


class InvalidRequest(Exception):
    error = "invalid_request"


class InvalidScope(Exception):
    error = "invalid_scope"


class UnsupportedGrantType(Exception):
    error = "unsupported_grant_type"


class UnsupportedResponseType(Exception):
    error = "unsupported_response_type"
