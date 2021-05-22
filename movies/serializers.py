from django.db.models import fields
from rest_framework import serializers
from .models import Movie, Rating, Mymovie

class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('movie', 'user')

class MymovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    rating_count = serializers.IntegerField(source='ratings.count', read_only=True)

    class Meta:
        model = Mymovie
        fields = '__all__'
        read_only_fields = ('movie', 'user')


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    rating_count = serializers.IntegerField(source='ratings.count', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    rating_count = serializers.IntegerField(source='ratings.count', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'