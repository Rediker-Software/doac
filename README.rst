Django OAuth2 Consumer (doac) |Build Status|
============================================

django-oauth2-consumer (DOAC) is a reusable application that can be used
to provide an OAuth2 cosumer for your project. It is based on `RFC
6749 <http://tools.ietf.org/html/rfc6749>`__ for the `OAuth2
authorization framework <http://oauth.net/2/>`__.

This project is in active development in the alpha stage. It is not
recommended for use in production and is not complete.

What do I need to use this?
---------------------------

-  Django 1.3+
-  Django `authentication
   application <https://docs.djangoproject.com/en/1.5/topics/auth/>`__
-  Python 2.6+

This plugin has not been tested on other configurations. If it works
with different requirements, or if a requirement is missing from the
list, feel free to bring up an issue.

What else does this have support for?
-------------------------------------

-  Django `admin
   application <https://docs.djangoproject.com/en/1.5/ref/contrib/admin/>`__

Where is the documentation?
---------------------------

The documentation is not complete, but we try our best to keep them
current and comprehensive.

`You can view them here on
ReadTheDocs. <https://django-oauth2-consumer.readthedocs.org/en/latest/>`__

Where are the tests?
--------------------

We are trying our best to keep them up to date. Feel free to submit a
pull request with tests for code that is missing it.

| You can run the tests with:
| ``python runtests.py``
| The test runner has support for coverage.py along with some other
options.

.. |Build Status| image:: https://travis-ci.org/kevin-brown/doac.png?branch=master
   :target: https://travis-ci.org/kevin-brown/doac
