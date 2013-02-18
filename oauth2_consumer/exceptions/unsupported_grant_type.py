from .base import UnsupportedGrantType


class GrantTypeNotDefined(UnsupportedGrantType):
    reason = "The grant type was malformed or invalid."


class GrantTypeNotValid(UnsupportedGrantType):
    reason = "The provided grant type is not supported."
