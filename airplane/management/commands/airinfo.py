# airinfo command
from __future__ import print_function
import os

from django.conf import settings
from django.core.management.base import BaseCommand

import airplane
from airplane.utils import get_cache_path, reverse_convert_url

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

        files = []
        for name in os.listdir(path):
            files.append(reverse_convert_url(name))

        print('Cache contents:')
        files.sort()
        for name in files:
            print('  ', name)

        print()
