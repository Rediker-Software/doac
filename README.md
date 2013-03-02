# Django OAuth2 Consumer (django-oauth2-consumer)

[![Build Status](https://travis-ci.org/kevin-brown/django-oauth2.png?branch=master)](https://travis-ci.org/kevin-brown/django-oauth2)

django-oauth2-consumer (DOAC) is a reusable application that can be used to provide an OAuth2 cosumer for your project.  It is based on [RFC 6749](http://tools.ietf.org/html/rfc6749) for the [OAuth2 authorization framework](http://oauth.net/2/).

This project is in active development in the alpha stage.  It is not recommended for use in production and is not complete.

## What do I need to use this?
- Django 1.5
- Django [authentication application](https://docs.djangoproject.com/en/1.5/topics/auth/)
- Python 2.7

This plugin has not been tested on other configurations.  If it works with different requirements, or if a requirement is missing from the list, feel free to bring up an issue.

## What else does this have support for?
- Django [admin application](https://docs.djangoproject.com/en/1.5/ref/contrib/admin/)

## Where is the documentation?
The documentation is not complete, but we try our best to keep them current and comprehensive.

[You can view them here on ReadTheDocs.](https://django-oauth2-consumer.readthedocs.org/en/latest/)

## Where are the tests?
We are trying our best to keep them up to date.  Feel free to submit a pull request with tests for code that is missing it.

You can run the tests with:
```
python runtests.py
```
The test runner has support for coverage.py along with some other options.
