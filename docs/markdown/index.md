Welcome to Django OAuth2 Consumer's documentation!
==================================================

Django OAuth2 Consumer (DOAC) is a reusable application that can be used to provide an OAuth consumer for your project.

* [Installation](installation.md)
* [API](api.md)
 * [Exceptions](exceptions/index.md)
 * [Models](models/index.md)
 * [Utilities](utilities.md)
 * [Views](views/index.md)
* [Settings](settings.md)

Requirements
============

We tried to make it so that this application did not require anything, but that is pretty illogical when you think about it, so we settled with a short list of requirements that should fit your project anyway. This application may work on different setups, but we probably haven't tested them, so contact us if you find that there is an issue with our list of requirements.

Required
--------

-   Django 1.3+
-   Django [authentication application](https://docs.djangoproject.com/en/1.5/topics/auth/)
-   Python 2.6+

This application is directly compatible with other tools and applications, but if you aren't using them it shouldn't make a difference. We provide extra functionality by default if it makes sense to do so.

Optional
--------

-   Django [admin application](https://docs.djangoproject.com/en/1.5/ref/contrib/admin/)

Getting Help
============

If you find a bug, have an idea for a feature, or just need some guidance, we provide support through our GitHub repository. Just open up a new issue and make sure to include as much information as possible so we can try our best to determine the problem. A working test case or example is always preferred, though we recognize that it is not always possible to provide one.

The issue tracker is available here: <https://github.com/kevin-brown/doac/issues>

Contributing
============

Django OAuth2 Consumer is an open-source application which you can contribute to. We will provide instructions for those interested in the future.
