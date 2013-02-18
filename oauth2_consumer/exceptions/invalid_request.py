from .base import InvalidRequest


class AuthorizationCodeAlreadyUsed(InvalidRequest):
    reason = "The authorization code was already used to get a refresh token."


class AuthorizationCodeNotProvided(InvalidRequest):
    reason = "The authorization code was malformed or invalid."


class AuthorizationCodeNotValid(InvalidRequest):
    reason = "The authorization code was malformed or invalid."


class ClientNotProvided(InvalidRequest):
    reason = "The client was malformed or invalid"


class RedirectUriDoesNotValidate(InvalidRequest):
    reason = "The reidrect URI does not validate against the client host."
    can_redirect = False


class RedirectUriNotProvided(InvalidRequest):
    reason = "The redirect URI was malformed or invalid."
    can_redirect = False


class ResponseTypeNotDefined(InvalidRequest):
    reason = "The request type was malformed or invalid."
