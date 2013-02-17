===============
Base Exceptions
===============

.. module:: oauth2_consumer.exceptions

.. exception:: InvalidRequest
   
   The :exc:`InvalidRequest` exception is raised because a parameter did not pass validation or was not provided.  The OAuth ``error`` for this exception is ``invalid_request``.
   
   This can be raised during the initial authorization request because:
   
   - A required parameter was not provideed.
   - A supplied parameter failed its verification check.
   
   This exception is not intended to be redirected to the client during the authorization stage.

.. exception:: InvalidScope
   
   The :exc:`InvalidScope` exception is raised because the scope that was provided for the request does not pass validation or was not provided.  The OAuth ``error`` for this exception is ``invalid_scope``.

.. exception:: ResponseTypeNotValid
   
   The :exc:`ResponseTypeNotValid` is raised during the initial authorization step because the requested ``response_type`` was not supported.  The OAuth ``error`` for this exception is ``unsupported_response_type``.
