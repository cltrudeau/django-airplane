# airplane.templatetags.airplanetags.py
import os

from django import template
from django.conf import settings
from django.utils.http import urlquote_plus

import requests

import airplane as package

register = template.Library()

# ============================================================================

def _convert_url(url):
    converted = urlquote_plus(url)
    converted = converted.replace('%', '')
    return converted


@register.simple_tag
def airplane(url):
    """This template tag modifies a URL depending on the values in settings.
    It either returns the URL as is, returns the URL as is and caches a copy,
    or returns a re-written URL pointing to the cache.
    
    Example::

        {% airplane 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css' %}
    """
    debug = getattr(settings, 'DEBUG', False)
    if not debug:
        # we are not in debug mode, just pass through the URL
        return url

    conf = getattr(settings, 'AIRPLANE_MODE', 0)
    if conf == 0:
        # not in AIRPLANE_MODE, pass through
        return url

    # convert url to local path
    filename = _convert_url(url)
    dirname = getattr(settings, 'AIRPLANE_CACHE', package.CACHE_DIR)

    if os.path.isabs(dirname):
        dir_path = dirname
    else:
        dir_path = os.path.join(getattr(settings, 'BASE_DIR'), dirname)

    file_path = os.path.join(dir_path, filename)

    if conf == package.BUILD_CACHE:
        # fetch the content for caching
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        response = requests.get(url, stream=True)
        if not response.ok:
            raise IOError('Unable to fetch %s' % url)
        with open(file_path, 'wb') as stream:
            for chunk in response.iter_content(chunk_size=128):
                stream.write(chunk)

    # we're caching, return the re-written static URL, need to encode
    return '/static/%s' % filename
