from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=300)
    release_date = models.DateField()
    genres = models.CharField(max_length=100)
    popularity = models.IntegerField()
    overview = models.TextField(blank=True)

    def __str__(self):
        return self.title

    # def natural_key(self):
    #     return (str(self.user), self.genres)

    
class Rating(models.Model):
    comment = models.CharField(max_length=255)
    score = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    
    def __str__(self):
        return f'{self.user.username}: {self.score}'

class Mymovie(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="mymovies")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mymovies")
    
class Recommand(models.Model):
    pass