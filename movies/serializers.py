from django.db.models import fields
from rest_framework import serializers
from .models import Movie, Rating, Mymovie

class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('movie', 'user')

class Mymovie(serializers.ModelSerializer):

    pass


class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('poster_path', 'title', )