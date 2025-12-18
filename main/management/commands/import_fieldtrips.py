from django.core.management.base import BaseCommand
import csv
from main.models import FieldTrip

class Command(BaseCommand):
    help = "This is how you import Field Trips from a .csv"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to csv file')

    def handle(self, *args, **options):
        file_path = options['csv_path']
        with open (file_path, newline='') as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                field_trip, created = FieldTrip.objects.get_or_create(
                    year = int(row['year']),
                    region = row['region'],
                    defaults = {'name': row.get('name') or None}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {field_trip.year} - {field_trip.region}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {field_trip.year} - {field_trip.region}. Entry skipped."))
                                      


