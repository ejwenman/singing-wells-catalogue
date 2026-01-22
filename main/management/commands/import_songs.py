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
                csv_name = row['name']
                archive_id = row['archive_id']
                csv_group = row['group']
                csv_visit = row['visit_id']
                csv_instruments = row['instruments'].split(",")
                csv_instruments = [str(i).strip() for i in csv_instruments]
                csv_audio_path = f"/singing_wells_media_archive/{row['audio_path']}"
                csv_youtube = row ['youtube']

                # Check if visit exists. Skip if not.
                try:
                    visit = Visit.objects.get(archive_id=csv_visit)
                except Visit.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"ERROR: Visit {csv_visit} does not exist. Skipping song {archive_id}."))
                    continue 

                # Check if group exists, or create it
                group, created = Group.objects.get_or_create(
                    name=csv_group,
                    origin=''
                )
                if created:
                    self.stdout.write(self.style.WARNING(f"Group {group.name} did not exist. Group created"))

                # Check if song already exits, or create it                    
                song, created = Song.objects.get_or_create(
                    archive_id=archive_id,
                    defaults={
                        'name': csv_name,
                        'group': group,
                        'visit': visit,
                        'audio_path': csv_audio_path,
                        'youtube': csv_youtube
                    })
                
                if not created:
                    song.name = csv_name
                    song.group = group
                    song.visit = visit
                    song.audio_path = csv_audio_path
                    song.youtube = csv_youtube
                    song.save()
                    song.instruments.clear()
                    self.update_instruments(song, csv_instruments)
                    self.stdout.write(self.style.WARNING(f"Updated song {song.name}"))

                if created:
                    self.update_instruments(song, csv_instruments)
                    self.stdout.write(self.style.SUCCESS(f"Created song {song.name}"))
       
    def update_instruments (self, song, instruments):
        for entry in instruments:
            try:
                instrument = Instrument.objects.get(name=entry)
            except Instrument.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Trying to add instrument '{entry}', but it does not exist. Create instrument (y/n)?."))
                answer = str(input())
                if answer == 'y':
                    instrument = Instrument.objects.create(name=entry)
                    self.stdout.write(self.style.SUCCESS(f"Created instrument {instrument.name}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Instrument {entry} not created. Did not add to song."))
                    continue  
            song.instruments.add(instrument)