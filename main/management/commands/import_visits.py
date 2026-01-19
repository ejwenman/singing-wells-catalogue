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
                try:
                    date_object = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    csv_field_trip = row['field_trip_id']

                    try:
                        field_trip = FieldTrip.objects.get(archive_id=csv_field_trip)
                    except FieldTrip.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Field Trip not found: {csv_field_trip} – Skipping Visit."))
                        continue

                    visit, created = Visit.objects.get_or_create(
                        archive_id = row['archive_id'],
                        defaults = {
                            'date': date_object,
                            'location': row['location'],
                            'field_trip': field_trip})
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created: {visit.archive_id}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Already exists: {visit.archive_id}. Entry skipped."))
                except:
                    self.stdout.write(self.style.WARNING(f"Something wrong with {row['archive_id']}. Skipping visit." ))
