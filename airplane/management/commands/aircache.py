# aircache command

from django.core.management.base import BaseCommand
from airplane.utils import cache_url, get_cache_path, convert_url

class Command(BaseCommand):
    help = 'Caches any URLs passed in as arguments in the airplane cache'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        dir_path = get_cache_path()

        for url in options['url']:
            filename = convert_url(url)
            cache_url(dir_path, filename, url)
