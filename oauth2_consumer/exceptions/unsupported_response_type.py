from .base import UnsupportedResponseType


class ResponseTypeNotValid(UnsupportedResponseType):
    reason = "The request type was malformed or invalid."