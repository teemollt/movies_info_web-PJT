from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=300)
    release_date = models.DateField()
    genres = models.CharField(max_length=100)
    popularity = models.IntegerField()
    overview = models.TextField(blank=True)
    