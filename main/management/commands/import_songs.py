from django.core.management.base import BaseCommand
import csv
from main.models import Song, FieldTrip, Group, Instrument, Visit

class Command(BaseCommand):
    help = "Import songs from a csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help="add csv path")

    def handle(self, *args, **options):
        file_path = options['csv_path']
        with open(file_path, newline='') as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                csv_group = row['group']
                csv_visit = row['visit_id']
                csv_instruments = row['instruments'].split(",")
                csv_instruments = [str(i).strip() for i in csv_instruments]
                try:
                    group = Group.objects.get(name=csv_group)
                except Group.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"ERROR: Group {csv_group} does not exist. Skipping entry."))
                    continue
                try:
                    visit = Visit.objects.get(visit_id=csv_visit)
                except Visit.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"ERROR: Visit {csv_visit} does not exist. Skipping entry."))
                    continue                       
                song, created = Song.objects.get_or_create(
                    name=row['name'],
                    group=group,
                    defaults={
                        'visit': visit,
                        'audio_path': f"/static/audio/songs{row['audio_path']}"
                    })
                if created:
                    for entry in csv_instruments:
                        print (f"Looking for instrument {entry}")
                        try:
                            instrument = Instrument.objects.get(name=entry)
                        except Instrument.DoesNotExist:
                            self.stdout.write(self.style.NOTICE(f"Instrument {entry} does not exist. Create instrument (y/n)?."))
                            answer = str(input())
                            if answer == 'y':
                                instrument = Instrument.objects.create(name=entry)
                                self.stdout.write(self.style.SUCCESS(f"Created instrument {instrument.name}"))
                            else:
                                self.stdout.write(self.style.Error(f"Instrument {entry} not created. Did not add to song."))
                                continue  
                        song.instruments.add(instrument)
                    self.stdout.write(self.style.SUCCESS(f"Created song {song.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {song.name}. Entry skipped."))

            
        
