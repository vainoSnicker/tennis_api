from django.core.management.base import BaseCommand, CommandError
from data_importer.data_importer import CSVImporter


class Command(BaseCommand):
    help = 'Init data'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start_year', type=int, help='Start year for init')

    def handle(self, *args, **kwargs):
        start_year = kwargs['start_year']
        if not start_year:
            raise CommandError('start year needed')
        CSVImporter().data_from_csv(start_year)
