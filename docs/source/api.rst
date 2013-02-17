===
API
===

Django OAuth2 Consumer comes with multiple models and utility functions which can be used to manage all of the tokens that are used with OAuth2.

Models
~~~~~~

.. class:: oauth2_consumer.models.Client
   
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
