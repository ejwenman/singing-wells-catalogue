from django.contrib import admin
from .models import FieldTrip, Visit, Group, Song, Instrument

admin.site.register(FieldTrip)
admin.site.register(Visit)
admin.site.register(Group)
admin.site.register(Instrument)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'visit', 'audio_path']
    list_filter = ['group', 'visit']
    filter_horizontal = ('instruments',)

