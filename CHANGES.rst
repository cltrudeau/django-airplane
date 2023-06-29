1.1.1
=====

* 2023/06/29
* Changed test suite to Python 3.8-3.11, Django 4.1, 4.2 (old versions dropped)

1.1
===

* URL to filename re-writing mechanism was creating files that didn't work on
Windows, changed how the files are named and stored

1.0
===

* add AUTO_CACHE feature that fetches if url isn't in the cache
* added support for schemaless urls
* removed support for Python 2
* updated dependancies to recent versions


0.3.1
=====

* fixing a merge conflict that got missed

0.3
===

* updated dependancies to working versions
* updated minimum django to secure 2.0.2, added tox testing for 2.1.2
* deprecated python 3.5
* changed wheel to build universal
* upgraded packages in requirements.txt for minimum versions in testing
* moved minimum version of python3 to 3.6
* changed tox testing for django 1.11, 2.1, 2.2

0.2
===

* **BREAKING CHANGE**: changed cache filename format
* added management commands for listing and adding to cache
* changed testing to be against django 1.11, 2.0 

0.1.1
=====

* changes to solve pip install problems with versions

0.1
===

* initial commit to pypi
