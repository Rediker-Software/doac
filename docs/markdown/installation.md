Installation
============

Django OAuth2 Consumer (DOAC) is on PyPi!

Using Pip
---------

> pip install doac

Then all you need to do is add `doac` to your `INSTALLED_APPS`.

```
INSTALLED_APPS = (
    ...
    "doac",
)
```

And set up the tables for everything.

```
python manage.py syncdb
```

Doing it manually
-----------------

You can still manually install DOAC, but it is recommended to install it using `pip`.

### 1. Copy DOAC Files

Copy the files from GitHub into your project directory to a folder called `doac`.

### 2. Add DOAC to your settings

Add `doac` to your `INSTALLED_APPS`.

### 3. Set up the database

Run `python manage.py syncdb` to install the tables for DOAC.
