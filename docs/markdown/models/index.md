======
Models
======

Django OAuth2 Consumer comes with multiple models which contain all of the tokens and other information that is used throughout the OAuth2 authorization process.

### *class* oauth2_consumer.models.<strong>Client</strong> ###
   
A single client that can be used when requesting an authorization.
   
<strong>name</strong>
      
The name of the client.  This will be used when the user is asked to approve any permissions that the client requests.
      
<strong>secret</strong>
      
The secret that is used to refresh tokens throughout the OAuth process.
   
<strong>access_host</strong>
      
The base URL that all `RedirectUri`'s will be validated against.
   
<strong>is_active</strong>
   
A boolean flag indicating whether or not the client can be used at all.
   
<strong>generate_secret()</strong>
      
Generates a secret string that meets the criteria of those which can be used for a client.
   
<strong>save(</strong><em>*args, **kwargs</em><strong>)</strong>
      
Saves the client to the database.  A secret is automatically generated for the client and can be retrieved using `secret`.  Any time a client is changed, a new secret is generated for it.

### *class* oauth2_consumer.models.<strong>RedirectUri</strong> ###
   
The url that a user can be redirected to during the authorization process.
  
<strong>client</strong>
      
The client that the url is tied to.  It must be under the `~Client.access_host` of the `Client` in order to be used.
   
<strong>url</strong>
      
The url that can be used.  It must be exactly the same when starting the authorization process.

### *class* oauth2_consumer.models.<strong>Scope</strong> ###
   
A scope that can be requested by a client as a permission.
   
<strong>short_name</strong>
      
The name of the scope that is used when a client is requesting a set of scopes to be authorized for.
   
<strong>full_name</strong>
      
The full name of the scope, it will be used during the approval process when telling a user what the client is requesting.
   
<strong>description</strong>
      
A short description of exactly what the scope will give the client access to.