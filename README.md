# Django OAuth2 Consumer (doac) [![Build Status](https://travis-ci.org/Rediker-Software/doac.png?branch=master)](https://travis-ci.org/Rediker-Software/doac)

DOAC is a reusable application that can be used to provide an OAuth2 cosumer for your project.  It is based on [RFC 6749](http://tools.ietf.org/html/rfc6749) for the [OAuth2 authorization framework](http://oauth.net/2/).

## What do I need to use this?
- Django 1.3+
- Django [authentication application](https://docs.djangoproject.com/en/1.5/topics/auth/)
- Python 2.6+

This plugin has not been tested on other configurations.  If it works with different requirements, or if a requirement is missing from the list, feel free to bring up an issue.

## What else does this have support for?
- Django [admin application](https://docs.djangoproject.com/en/1.5/ref/contrib/admin/)
- [Django Rest Framework](http://django-rest-framework.org/) - [Instructions](docs/integrations.md)

## Where is the documentation?
The documentation is not complete, but we try our best to keep them current and comprehensive.

They are included in this repository in markdown versions.  [You can view them here.](docs/index.md)

## Where are the tests?
We are trying our best to keep them up to date.  Feel free to submit a pull request with tests for code that is not covered.

You can run the tests with:
```
python runtests.py
```
The test runner has support for coverage.py along with some other options.
