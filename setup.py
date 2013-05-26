#!/usr/bin/env python

from setuptools import setup, find_packages
import os
from doac import __version__

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(PACKAGE_DIR)


setup(name='doac',
      version=__version__,
      url="https://github.com/kevin-brown/django-oauth2",
      author="Kevin Brown",
      author_email="kbrown@rediker.com",
      description="An OAuth2 Consumer application for your Django project.",
      long_description=file(os.path.join(PACKAGE_DIR, 'README.rst')).read(),
      license="MIT",
      packages=find_packages(exclude=["tests*", ]),
      include_package_data=True,
      install_requires=[
          'Django>=1.3',
          'simplejson>=1.5',
      ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ]
)
