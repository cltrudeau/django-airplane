# airinfo command
from django.conf import settings
from django.core.management.base import BaseCommand

import airplane
from airplane.utils import get_cache_path, cache_dict

class Command(BaseCommand):
    help = ('Shows information about the airplane app, including the mode, ',
        'the cache directory and what is in the cache')

    def handle(self, *args, **options):
        conf = getattr(settings, 'AIRPLANE_MODE', 0)
        if conf == airplane.USE_CACHE:
            mode = 'USE_CACHE'
        elif conf == airplane.BUILD_CACHE:
            mode = 'BUILD_CACHE'
        elif conf == airplane.AUTO_CACHE:
            mode = 'AUTO_CACHE'
        else:
            mode = 'OFF'

        print('Cache mode:', mode)

        path = get_cache_path()
        print('Cache directory:', path)

        print('Cache contents:')
        d = cache_dict()
        for url, name in d.items():
            print('file:', name, 'caches:')
            print('    ', url)

        print()
