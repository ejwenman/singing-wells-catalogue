from django.core.management.base import BaseCommand
import csv
from main.models import Group

class Command(BaseCommand):
    help = "Script for importing group details from a .csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='adding CSV path')

    def handle(self, *args, **options):
        file_path = options['csv_path']
        with open (file_path, newline='') as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                group, created = Group.objects.get_or_create(
                    name = row['name'],
                    defaults = {'origin': row['origin']})
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {group.name}, {group.origin}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {group.name}. Entry skipped."))
