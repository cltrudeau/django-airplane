from pathlib import Path
import uuid 
import requests

from django.conf import settings
from django.utils.http import urlquote_plus

from airplane.pathing import get_cache_path

# =============================================================================

url_filename_map = None

# =============================================================================
# Filename Mapping Methods
# =============================================================================

def read_cache_map():
    ### Reads cache-filename-map from the hard drive and (re-)builds the dict
    cache_map = Path(get_cache_path()) / 'cache_map'

    global url_filename_map
    url_filename_map = {}
    if cache_map.exists():
        with cache_map.open() as f:
            for line in f:
                name, url = line.split(':', 1)
                url_filename_map[url] = name


def write_cache_map():
    global url_filename_map
    if not url_filename_map:
        return

    cache_dir = Path(get_cache_path())
    if not cache_dir.exists():
        cache_dir.mkdir()

    cache_map = cache_dir / 'cache_map'

    # write name:url pairs to the file
    output = [f'{name}:{url}' for url,name in url_filename_map.items()]
    cache_map.write_text('\n'.join(output))

# =============================================================================
# Cache Handling
# =============================================================================

def cached_filename(url):
    """Returns the filename for the cached url"""
    global url_filename_map
    read_cache_map()

    try:
        filename = url_filename_map[url]
    except KeyError:
        # nothing in the cache_map file, try the old filename mapping method
        filename = urlquote_plus(url)
        filename = filename.replace('%', '|')

    path = Path(get_cache_path()) / filename
    if path.exists():
        return filename

    # something has gone wrong, can't find the file
    raise IOError(f'could not find file *{filename}* for url *{url}*')


def cache_url(url):
    read_cache_map()

    # get the filename, or create a new one
    try:
        filename = url_filename_map[url]
    except KeyError:
        # filename should end in the same thing the URL does so that django's
        # static serve can guess its mimetype
        _, dot, ext = url.rpartition('.')
        filename = str(uuid.uuid4().hex)

        if dot == '.':
            filename = filename + '.' + ext

        url_filename_map[url] = filename

    if url.startswith('//'):
        # schemaless, make an assumption
        url = 'https:' + url

    response = requests.get(url, stream=True)
    if not response.ok:
        raise IOError('Unable to fetch %s' % url)

    cache_dir = Path(get_cache_path())
    if not cache_dir.exists():
        cache_dir.mkdir()

    content = cache_dir / filename
    with content.open('wb') as stream:
        for chunk in response.iter_content(chunk_size=128):
            stream.write(chunk)

    write_cache_map()


def cache_exists(url):
    try:
        cached_filename(url)
    except IOError:
        return False

    return True


def cache_dict():
    global url_filename_map
    read_cache_map()
    return url_filename_map
