from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Song, Instrument, FieldTrip, Group
import math

def view_songs(request):

    songs = Song.objects.all()
    instruments = Instrument.objects.all()
    trips = FieldTrip.objects.all()
    groups = Group.objects.all()
    context = {
        'songs':songs,
        'instruments':instruments,
        'trips':trips,
        'groups':groups,
        }
    return render(request, 'main/base.html', context)

def songs_api(request):

    if request.method == "GET":
        params = request.GET
        filter = {}
        for key in params:
            value_list = []
            for value in params.getlist(key):
                value_list.append(value)
            filter.update({key:value_list})

        songs = Song.objects.all()
        returned_songs = []

        field_map = {
            'instrument': 'instruments',
            'group': 'group',
            'fieldTrip': 'visit.field_trip',
        }

        for song in songs:
            is_match = 1
            for field in filter:
                if not field in ['page', 'page_size']:
                    if is_match == 1:

                        #separating many-to-many / many-to-one field types
                        field_object = song._meta.get_field(field_map[field].split('.')[0])

                        if field_object.many_to_many:
                            selected_values = filter[field]
                            attribute = getattr(song, field_map[field])
                            for value in selected_values:
                                if not attribute.filter(name=value).exists():
                                    is_match = 0
                                    break

                        else:
                            # splitting map to chain getattr
                            levels = field_map[field].split(".")
                            # chaining getattr to get to the desired attribute. Starts from song object, but then loops until no more levels.
                            attribute = getattr(song, levels[0])
                            for level in levels[1:]:
                                attribute = getattr(attribute, level)

                            items = filter[field]
                            if not str(attribute) in items:
                                is_match = 0

            if is_match == 1:
                returned_songs.append(song)
       
        page_number = int(filter.get('page', [1])[0])
        page_size = int(filter.get('page_size', [20])[0])

        total_pages = max(1, math.ceil(len(returned_songs)/page_size))
        song_start = ((page_number-1)*(page_size))
        song_end = ((page_number)*(page_size))
        returned_songs = returned_songs[song_start:song_end]


        songs_data = []
        for song in returned_songs:
            audio_url = song.audio_path if song.audio_path else "n/a"
            instruments = []
            for instrument in song.instruments.all():
                instruments.append(instrument.name)
            songs_data.append({
                'name': song.name,
                'group': song.group.name,
                'visit': song.visit.location,
                'audio_url': audio_url,
                'instruments': instruments,
            })
        context = {
            'songs':songs_data,
            'pages':total_pages,
        }

        return JsonResponse(context)
