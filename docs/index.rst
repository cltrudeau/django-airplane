.. include:: ../README.rst

Version
=======

Version: |version|

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Other Projects
==============

When I first decided to write this I went looking for similar projects.  A
similar project exists called ``django-offlinecdn`` written by Gabriel Gabster.
His approach is slightly different in that the tag acts as a wrapper for
multiple lines of HTML and finds all URLs contained within.  This may be more
efficient as it only needs to run once, but has dependencies on Beautiful Soup
to do URL parsing.  In case you'd prefer his implementation it is available
here: https://github.com/gabegaster/django-offlinecdn
