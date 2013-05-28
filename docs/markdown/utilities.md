DOAC Utilities
==============

DOAC comes with a few utilities which make it easier to use DOAC.  All of the utilities are located in the `utils.py` file.

`doac.utils.`prune_old_authorization_codes()
--------------------------------------------
Prunes all authorization codes which have expired.  The codes may be pruned automatically if enabled within the settings.  In this case, the codes will be automatically pruned each time that a user tries to authorize themselves.

`doac.utils.`get_handler(`handler_name`)
----------------------------------------
Returns the class for the handler given the full path.  It will automatically import the class from the given file.  **Note:** the handler will only be imported if it is located within the specified list of handlers.

`doac.utils.`request_error_header(`exception`)
----------------------------------------------
Generates the `WWW-Authenticate` header that must be supplied for errors that occur during various parts of the authorization and authentication process.

`doac.utils.`total_seconds(`delta`)
-----------------------------------
Returns the total number of seconds from a `timedelta`.
