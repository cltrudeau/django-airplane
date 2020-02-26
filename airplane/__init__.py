__version__ = '1.0.0'

CACHE_DIR = '.airplane_cache'

USE_CACHE   = 1
BUILD_CACHE = 2
AUTO_CACHE = 3

from airplane.utils import get_cache_path as cache_path
