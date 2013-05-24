from .base import AccessDenied


class AuthorizationDenied(AccessDenied):
    reason = "The request for permission was denied."
