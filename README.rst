django-airplane
***************

This app is to help in those situations where you can't get on the network but
you want to write some Django code.  Surround your static CDN references (like
jquery and the like) with this template tag and when you turn it on the URLs
will be re-written from a local copy.

Installation
============

In your settings file, add 'airplane' to your ``settings.INSTALLED_APPS`` field
and make the following additions:

.. code-block:: python

    import airplane

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, airplane.CACHE_DIR),
    )

    AIRPLANE_MODE = airplane.BUILD_CACHE
    #AIRPLANE_MODE = airplane.USE_CACHE

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
``AIRPLANE_MODE`` value set to either ``airplane.BUILD_CACHE`` or
``airplane.USE_CACHE``.  If one of these conditions is not met, the tag simply
returns the value passed in.

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

Once you have cached all the files you are using, switch ``AIRPLANE_MODE`` to
``airplane.USE_CACHE``.  All URLs are now re-written to point to the contents
of the local cache.

Supports
========

django-airplane has been tested with:

* Python 2.7, 3.6 and Django 1.11 
* Python 3.6, 3.7 and Django 2.0.2
* Python 3.6, 3.7 and Django 2.1.2

Older versions of Django should still work but aren't tested against.

Docs
====

Docs available at: http://django-airplane.readthedocs.io/en/latest/

Source: https://github.com/cltrudeau/django-airplane
