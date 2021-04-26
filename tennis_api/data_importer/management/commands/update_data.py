from datetime import date
from django.core.management.base import BaseCommand, CommandError
from data_importer.data_importer import CSVImporter


class Command(BaseCommand):
    help = 'Update data'

    def handle(self, *args, **kwargs):
        CSVImporter().data_from_csv(date.today().year, False)
