======
Models
======

Django OAuth2 Consumer comes with multiple models which contain all of the tokens and other information that is used throughout the OAuth2 authorization process.

.. module:: oauth2_consumer.models

.. class:: Client
   
   A single client that can be used when requesting an authorization.
   
   .. attribute:: name
      
      The name of the client.  This will be used when the user is asked to approve any permissions that the client requests.
      
   .. attribute:: secret
      
      The secret that is used to refresh tokens throughout the OAuth process.
   
   .. attribute:: access_host
      
      The base URL that all :class:`RedirectUri`'s will be validated against.
   
   .. attribute:: is_active
      
      A boolean flag indicating whether or not the client can be used at all.
   
   .. method:: generate_secret()
      
      Generates a secret string that meets the criteria of those which can be used for a client.
   
   .. method:: save(*args, **kwargs)
      
      Saves the client to the database.  A secret is automatically generated for the client and can be retrieved using :attr:`secret`.  Any time a client is changed, a new secret is generated for it.

.. class:: RedirectUri
   
   The url that a user can be redirected to during the authorization process.
   
   .. attribute:: client
      
      The client that the url is tied to.  It must be under the :attr:`~Client.access_host` of the :class:`Client` in order to be used.
   
   .. attribute:: url
      
      The url that can be used.  It must be exactly the same when starting the authorization process.

.. class:: Scope
   
   A scope that can be requested by a client as a permission.
   
   .. attribute:: short_name
      
      The name of the scope that is used when a client is requesting a set of scopes to be authorized for.
   
   .. attribute:: full_name
      
      The full name of the scope, it will be used during the approval process when telling a user what the client is requesting.
   
   .. attribute:: description
      
      A short description of exactly what the scope will give the client access to.
