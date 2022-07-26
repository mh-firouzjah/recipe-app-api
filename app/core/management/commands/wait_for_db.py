import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    '''Django Command to pause execution until db is available'''

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_con = None
        while not db_con:
            try:
                db_con = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 seconds...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
