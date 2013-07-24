from .base import InvalidRequest


class AuthorizationCodeAlreadyUsed(InvalidRequest):
    reason = "The authorization code was already used to get a refresh token."


class AuthorizationCodeNotProvided(InvalidRequest):
    reason = "The authorization code was not provided."


class AuthorizationCodeNotValid(InvalidRequest):
    reason = "The authorization code was malformed or invalid."


class ClientNotProvided(InvalidRequest):
    reason = "The client was not provided."


class ClientSecretNotProvided(InvalidRequest):
    reason = "The client secret was not provided."


class CredentialsNotProvided(InvalidRequest):
    reason = "No credentials were provided to authenticate the request to view this page."


class RedirectUriDoesNotValidate(InvalidRequest):
    reason = "The redirect URI does not validate against the client host."
    can_redirect = False


class RedirectUriNotProvided(InvalidRequest):
    reason = "The redirect URI was not provided."
    can_redirect = False


class RefreshTokenNotProvided(InvalidRequest):
    reason = "The refresh token was not provided."


class RefreshTokenNotValid(InvalidRequest):
    reason = "The refresh token was malformed or invalid."


class ResponseTypeNotProvided(InvalidRequest):
    reason = "The response type was not provided."
