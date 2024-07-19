import logging
import os

from django.core.management.base import BaseCommand

logger = logging.getLogger('django_project_api')


class Command(BaseCommand):
    help = 'CSV import product'

    def handle(self, *args, **options):
        home_dir = os.path.expanduser("~")
        logger.info("Custom Management Command")
