Settings
========

We think we set up Django OAuth2 Consumer with reasonable defualts, but there is always the option to change them through your central settings file.

All of these settings are available on the `OAUTH_CONFIG` dictionary.

`HANDLERS`
----------

This setting controls which handlers are acceptable for users to authenticate with. It should be specified as a tuple of strings which contain the full Python pathes to the middleware classes. If this is empty, users are not going to be able to authenticate with your project.

*Default*:

```
"HANDLERS": (
    "oauth2_consumer.handlers.bearer.BearerHandler",
)
```

`ACCESS_TOKEN`
--------------

This setting controls the settings for access tokens. It should be a dictionary containing any of the following keys:

### `EXPIRES`

A timedelta object representing the time after the creation of the token when the access token will expire and become invalid.

*Default*:

```
datetime.timedelta(hours=2)
```

`AUTHORIZATION_CODE`
--------------------

This setting controls the settings for the authorization code which is used during the authorization process. It should be a dictionary containing any of the following keys:

### `EXPIRES`

A timedelta object representing the time after the creation of the code when the authorization code will expire and become invalid.

*Default*:

```
datetime.timedelta(minutes=15)
```

`AUTHORIZATION_TOKEN`
---------------------

This setting controls the settings for the authorization token which is used after the authorization process. It should be a dictionary containing any of the following keys:

### `EXPIRES`

A timedelta object representing the time after the creation of the token when the authorization token will expire and become invalid.

*Defualt*:

```
datetime.timedelta(minutes=15)
```

`REFRESH_TOKEN`
---------------

This setting controls the settings for the refresh tokens which are used after the authorization process to retrieve access tokens. It should be a dictionary containing any of the folllwing keys:

### `EXPIRES`

A timedelta object which represents the time after the creation of the token when the refresh token will expire and become invalid.

*Default*:

```
datetime.timedelta(days=60)
```
