django-airplane
***************

This app is to help in those situations where you can't get on the network but
you want to write some Django code.  Surround your static CDN references (like
jquery and the like) with this template tag and when you turn it on the URLs
will be re-written from a local copy.

Installation
============

In your settings file, add 'airplane' to your ``settings.INSTALLED_APPS`` field:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'airplane',
    )

Also in settings, make the following additions:

.. code-block:: python

    import airplane

    STATICFILES_DIRS = (
        airplane.cache_path(),
    )

    AIRPLANE_MODE = airplane.BUILD_CACHE
    #AIRPLANE_MODE = airplane.USE_CACHE
    #AIRPLANE_MODE = airplane.AUTO_CACHE

Now use the ``airplane`` tag in your templates

.. code-block:: html

    {% load airplanetags %}

    <html>
        <head>
            <link rel="stylesheet"
                href="{% airplane 'https://maxcdn.bootstrapcdn.com/bootstrap.min.css' %}">
        </head>
    </html>

Change the ``AIRPLANE_MODE`` setting to ``airplane.USE_CACHE`` and subsequent
calls to the ``{% airplane %}`` tag will return a reference to the locally 
cached version.


Settings
========

Airplane only does something if ``DEBUG=True`` and if you have an
``AIRPLANE_MODE`` value set to ``airplane.BUILD_CACHE``,
``airplane.USE_CACHE``, or ``airplane.AUTO_CACHE``.  If one of these
conditions is not met, the tag simply returns the value passed in.

For example, if ``DEBUG=False`` and your template contains:

.. code-block:: html

    <link rel="stylesheet"
        href="{% airplane 'https://maxcdn.bootstrapcdn.com/bootstrap.min.css' %}">


Then the above snippet renders as:

.. code-block:: html

    <link rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap.min.css">


When ``AIRPLANE_MODE`` is set to ``airplane.BUILD_CACHE`` any URLs passed in
are fetched and their contents added to a local cache.  The default local
cache is ``.airport_cache`` relative to the base directory of your project.

You can change the location of the cache by setting ``AIRPLANE_CACHE``.  The
setting accepts either fully qualified paths or paths relative to the
project's base directory.

.. code-block:: python

    # settings.py

    AIRPLANE_CACHE = /foo/bar/cache     # fully qualified

    # or

    AIRPLANE_CACHE = my_cache           # relative to settings.BASE_DIR

    # or nothing, defaults to settings.BASEDIR + '.airplane_cache'


Once you have cached all the files you are using, switch ``AIRPLANE_MODE`` to
``airplane.USE_CACHE``.  All URLs are now re-written to point to the contents
of the local cache.

Alternatively, you can set ``AIRPLANE_MODE`` to ``airplane.AUTO_CACHE`` and
the first call will cache the file and subsequent calls will use the cached
copy.

Commands
========

The following django commands come with airplane.

airinfo
-------

.. code-block:: sh

    $ ./manage.py airinfo
    Cache mode: AUTO_CACHE
    Cache directory: /Users/foo/sample_site/.airplane_cache
    Cache contents:
       https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css


This command takes no arguments and displays information about the cache. The
current mode, the path of the directory and any items cached inside are shown.


aircache
--------

.. code-block:: sh

    ./manage.py aircache https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css

This command takes a single URL as an argument and caches the contents of the
URL.

Schemaless URLs
===============

As airplane is a template tag library, it doesn't have access to the request
object at execution. In order to allow schemaless URLs, the code makes the
assumption that the schema is "https" if it is not given in the URL.


Supports
========

django-airplane has been tested with:

* Python 3.6, 3.7 and Django 2.2
* Python 3.6, 3.7 and Django 3.0

Docs
====

Docs available at: http://django-airplane.readthedocs.io/en/latest/

Source: https://github.com/cltrudeau/django-airplane
