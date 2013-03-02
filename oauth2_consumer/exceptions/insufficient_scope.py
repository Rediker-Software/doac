from .base import InsufficientScope


class ScopeNotEnough(InsufficientScope):
    reason = "The access token does not have enough scope to access this page."
