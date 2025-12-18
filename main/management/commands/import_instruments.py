import csv
from django.core.management.base import BaseCommand
from main.models import Instrument

class Command(BaseCommand):
    help = "Script for importing instrument details from a .csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='adding CSV path')

    def handle(self, *args, **options):
        file_path = options['csv_path']
        with open(file_path, newline='') as f:
            csv_file = csv.DictReader(f) 
            for row in csv_file:
                instrument, created = Instrument.objects.get_or_create(name=row['name'])
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {instrument.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {instrument.name}. Entry skipped"))