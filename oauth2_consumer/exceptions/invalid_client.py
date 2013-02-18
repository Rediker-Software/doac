from .base import InvalidClient


class ClientSecretNotValid(InvalidClient):
    reason = "The client secret was malformed or invalid."