from django.db import models

# Create your models here.
class FieldTrip(models.Model):
    year = models.IntegerField()
    region = models.CharField(max_length=255)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.year} - {self.region}"

class Visit(models.Model):
    visit_id = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    field_trip = models.ForeignKey(FieldTrip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.visit_id}, {self.date} – {self.location}"
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField("Village/Place of Origin", max_length=50)

    def __str__(self):
        return self.name

class Instrument(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Song(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    visit = models.ForeignKey(
        Visit,
        on_delete=models.SET_NULL,
        null=True
    )
    audio_path = models.CharField(max_length=255, null=True)
    instruments = models.ManyToManyField(Instrument)

    def __str__(self):
        return self.name
