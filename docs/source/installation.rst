============
Installation
============

Django OAuth2 Consumer (DOAC) is not yet on PyPi, so you need to build it manually.

1. Copy DOAC Files
~~~~~~~~~~~~~~~~~~

Copy the files from GitHub into your project directory to a folder called ``oauth2_consumer``.

2. Add DOAC to your settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``oauth2_consumer`` to your ``INSTALLED_APPS``.

3. Set up the database
~~~~~~~~~~~~~~~~~~~~~~

Run ``python manage.py syncdb`` to install the tables for DOAC.
