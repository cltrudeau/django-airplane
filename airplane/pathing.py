from pathlib import Path

from django.conf import settings

def get_cache_path():
    from airplane.__init__ import CACHE_DIR
    path = Path(getattr(settings, 'AIRPLANE_CACHE', CACHE_DIR))

    if not path.is_absolute():
        path = Path(getattr(settings, 'BASE_DIR')) / path

    return path.resolve()

