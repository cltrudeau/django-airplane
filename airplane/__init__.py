__version__ = '1.1.0'

CACHE_DIR = '.airplane_cache'

USE_CACHE   = 1
BUILD_CACHE = 2
AUTO_CACHE = 3

from airplane.pathing import get_cache_path as cache_path 
_silence_pyflakes = cache_path 
