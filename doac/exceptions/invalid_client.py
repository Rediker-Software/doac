from .base import InvalidClient


class ClientDoesNotExist(InvalidClient):
    reason = "The client was malformed or invalid."


class ClientSecretNotValid(InvalidClient):
    reason = "The client secret was malformed or invalid."
