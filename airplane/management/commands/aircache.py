# aircache command

from django.core.management.base import BaseCommand
from airplane.utils import cache_url

class Command(BaseCommand):
    help = 'Caches any URLs passed in as arguments in the airplane cache'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['url']:
            cache_url(url)
