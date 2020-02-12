# airplane.templatetags.airplanetags.py
from django import template
from django.conf import settings

import airplane as package
from airplane.utils import get_cache_path, convert_url, cache_url, cache_exists

register = template.Library()

# ============================================================================

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
    filename = convert_url(url)
    dir_path = get_cache_path()

    if conf == package.BUILD_CACHE:
        cache_url(dir_path, filename, url)
    elif conf == package.AUTO_CACHE:
        if not cache_exists(dir_path, filename):
            cache_url(dir_path, filename, url)

    # we're caching, return the re-written static URL, need to encode
    return '/static/%s' % filename
