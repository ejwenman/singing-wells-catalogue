from django.core.management.base import BaseCommand
import csv
from main.models import Visit, FieldTrip
from datetime import datetime

class Command(BaseCommand):
    help = "Import visits from a .csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='adding CSV path')

    def handle(self, *args, **options):
        file_path = options['csv_path']
        with open (file_path, newline='') as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:

                date_object = datetime.strptime(row['date'], '%Y-%m-%d').date()
                field_trip_parts = row['field_trip'].split(' ', 1)
                year = int(field_trip_parts[0])
                region = field_trip_parts[1]

                try:
                    field_trip = FieldTrip.objects.get(year=year, region=region)
                except FieldTrip.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Field Trip not found: {year} {region} – Skipping Visit."))
                    continue

                visit, created = Visit.objects.get_or_create(
                    visit_id = row['visit_id'],
                    defaults = {
                        'date': date_object,
                        'location': row['location'],
                        'field_trip': field_trip})
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {visit.visit_id}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {visit.visit_id}. Entry skipped."))
