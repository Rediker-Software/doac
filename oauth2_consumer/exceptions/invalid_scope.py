from .base import InvalidScope


class ScopeNotDefined(InvalidScope):
    reason = "The scope was malformed or invalid."


class ScopeNotValid(InvalidScope):
    reason = "The scope contained values which were incorrect."