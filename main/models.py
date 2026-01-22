from django.db import models

# Create your models here.
class FieldTrip(models.Model):
    archive_id = models.CharField(max_length=50, unique=True)
    year = models.IntegerField()
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.year} - {self.country}, {self.region}"

class Visit(models.Model):
    archive_id = models.CharField(max_length=12, unique=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    field_trip = models.ForeignKey(FieldTrip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.archive_id}, {self.date} – {self.location}"
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField("Village/Place of Origin", max_length=50, null=True)

    def __str__(self):
        return self.name

class Instrument(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Song(models.Model):
    archive_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    visit = models.ForeignKey(
        Visit,
        on_delete=models.SET_NULL,
        null=True
    )
    audio_path = models.CharField(max_length=255, null=True)
    instruments = models.ManyToManyField(Instrument)
    youtube = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
