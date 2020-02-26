# airplane.templatetags.airplanetags.py
from django import template
from django.conf import settings

import airplane as package
from airplane.utils import cache_url, cached_filename, cache_exists

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

    # if in building mode, or in auto-mode and we need to build
    if conf == package.BUILD_CACHE or (conf == package.AUTO_CACHE and \
            not cache_exists(url)):
        cache_url(url)

    # we're caching, return the re-written static URL, need to encode
    return '/static/%s' % cached_filename(url)
