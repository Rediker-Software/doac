========
Settings
========

We think we set up Django OAuth2 Consumer with reasonable defualts, but there is always the option to change them through your central settings file.

All of these settings are available on the ``OAUTH_CONFIG`` dictionary.

HANDLERS
========
**Optional**

This setting controls which handlers are acceptable for users to authenticate with.  It should be specified as a tuple of strings which contain the full Python pathes to the middleware classes.  If this is empty, users are not going to be able to authenticate with your project.

*Default*

    "HANDLERS": (
        "oauth2_consumer.handlers.bearer.BearerHandler",
    )

ACCESS_TOKEN
============
**Optional**

This setting controls the settings for access tokens.  It should be a dictionary containing any of the following keys:

EXPIRES
-------
A timedelta object representing the time after the creation of the token when the access token will expire and become invalid.

*Default*

    datetime.timedelta(hours=2)

AUTHORIZATION_CODE
==================
**Optional**

AUTHORIZATION_TOKEN
===================
**Optional**

REFRESH_TOKEN
=============
**Optional**
