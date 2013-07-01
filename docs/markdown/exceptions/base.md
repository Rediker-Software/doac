===============
Base Exceptions
===============

.. module:: oauth2_consumer.exceptions.base

.. exception:: AccessDenied
   
   The :exc:`AccessDenied` exception is raised during the approval step of the authorization process if the user rejects the clients request for permission.  The OAuth ``error`` for this exception is ``access_denied``.

.. exception:: InvalidClient
   
   The :exc:`InvalidClient` exception is raised if a client was provided but had an error.

.. exception:: InvalidGrant

.. exception:: InvalidRequest
   
   The :exc:`InvalidRequest` exception is raised because a parameter did not pass validation or was not provided.  The OAuth ``error`` for this exception is ``invalid_request``.
   
   This can be raised during the initial authorization request because:
   
   - A required parameter was not provideed.
   - A supplied parameter failed its verification check.
   
   This exception is not intended to be redirected to the client during the authorization stage.

.. exception:: InvalidScope
   
   The :exc:`InvalidScope` exception is raised because the scope that was provided for the request does not pass validation or was not provided.  The OAuth ``error`` for this exception is ``invalid_scope``.

.. exception:: UnsupportedGrantType
   
   The :exc:`UnsupportedGrantType` exception is raised during the exchanging of tokens if the specified grant type is in the list of suppported grant types, or was not provided.

.. exception:: UnsupportedResponseType
   
   The :exc:`UnsupportedResponseType` exception is raised during the initial authorization step because the requested ``response_type`` was not supported.  The OAuth ``error`` for this exception is ``unsupported_response_type``.
