# Import all of the settings from the global settings file.
# This allows us to have our own custom settings for running tests.

from django.conf.global_settings import *
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS = [
    "django.contrib.auth",
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "oauth2_consumer",
    "tests",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "oauth2.db",
    }
}
