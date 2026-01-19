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
                csv_id = row['archive_id']
                csv_year = int(row['year'])
                csv_country = row['country']
                csv_region = row['region']
                csv_name = row.get('name')

                field_trip, created = FieldTrip.objects.get_or_create(
                    archive_id = csv_id,
                    defaults = {
                        'year': csv_year,
                        'country': csv_country,
                        'region': csv_region or None,
                        'name': csv_name or None,
                        }
                )

                if not created:
                    field_trip.archive_id = csv_id
                    field_trip.year = csv_year
                    field_trip.country = csv_country
                    field_trip.region = csv_region
                    field_trip.name = csv_name
                    field_trip.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated: {field_trip.year} - {field_trip.country}, {field_trip.region}"))

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {field_trip.year} - {field_trip.country}, {field_trip.region}"))
                                      


