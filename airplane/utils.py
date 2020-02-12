import os, requests

from django.conf import settings
from django.utils.http import urlquote_plus, urlunquote_plus

import airplane

def get_cache_path():
    dirname = getattr(settings, 'AIRPLANE_CACHE', airplane.CACHE_DIR)

    if os.path.isabs(dirname):
        dir_path = dirname
    else:
        dir_path = os.path.join(getattr(settings, 'BASE_DIR'), dirname)

    return dir_path


def convert_url(url):
    c = urlquote_plus(url)
    c = c.replace('%', '|')
    return c


def reverse_convert_url(name):
    r = name
    r = r.replace('|', '%')
    r = urlunquote_plus(r)
    return r


def cache_url(dir_path, filename, url):
    # fetch the content for caching
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_path = os.path.join(dir_path, filename)

    if url.startswith('//'):
        # schemaless, make an assumption
        url = 'https:' + url

    response = requests.get(url, stream=True)
    if not response.ok:
        raise IOError('Unable to fetch %s' % url)
    with open(file_path, 'wb') as stream:
        for chunk in response.iter_content(chunk_size=128):
            stream.write(chunk)


def cache_exists(dir_path, filename):
    file_path = os.path.join(dir_path, filename)
    return os.path.exists(file_path)
