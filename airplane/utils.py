from pathlib import Path
import json, uuid 
import requests

from django.utils.http import urlquote_plus

from airplane.pathing import get_cache_path

# =============================================================================

url_filename_map = None

# =============================================================================
# Filename Mapping Methods
# =============================================================================

def read_cache_map():
    ### Reads cache-filename-map from the hard drive and (re-)builds the dict

    # only read first time through
    global url_filename_map
    if url_filename_map is not None:
        return

    # url_filename_map is None, build the dict
    cache_map = Path(get_cache_path()) / 'cache_map.json'

    url_filename_map = {}
    if cache_map.exists():
        with cache_map.open() as f:
            url_filename_map = json.load(f)


def write_cache_map():
    global url_filename_map
    if not url_filename_map:
        return

    cache_dir = Path(get_cache_path())
    if not cache_dir.exists():
        cache_dir.mkdir()

    cache_map = cache_dir / 'cache_map.json'
    with cache_map.open('w') as output:
        json.dump(url_filename_map, output, indent=4)

# =============================================================================
# Cache Handling
# =============================================================================

def _create_path(filename):
    ### patching Path is problematic, so wrapping the call to Path in a
    # function so that can be patched during testing
    return Path(get_cache_path()) / filename


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

    try:
        path = _create_path(filename)
        if path.exists():
            return filename
    except OSError:
        # bad characters in the filename (old filename format on Windows, for
        # example) will blow up Path, ignore to fall out to error handler
        pass

    # something has gone wrong, can't find the file, return 
    return None


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

    fetch_url = url
    if url.startswith('//'):
        # schemaless, make an assumption
        fetch_url = 'https:' + url

    response = requests.get(fetch_url, stream=True)
    if not response.ok:
        raise IOError('Unable to fetch %s' % fetch_url)

    cache_dir = Path(get_cache_path())
    if not cache_dir.exists():
        cache_dir.mkdir()

    content = cache_dir / filename
    with content.open('wb') as stream:
        for chunk in response.iter_content(chunk_size=128):
            stream.write(chunk)

    url_filename_map[url] = filename
    write_cache_map()


def cache_exists(url):
    return cached_filename(url) is not None


def cache_dict():
    global url_filename_map
    read_cache_map()
    return url_filename_map
