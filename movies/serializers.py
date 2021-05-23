from django.db.models import fields
from rest_framework import serializers
from .models import Movie, Rating, Mymovie

class RatingSerializer(serializers.ModelSerializer):
    # movie = 
    movie_genre = serializers.CharField(source='movie.genres', read_only=True)
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('movie', 'user')
        # depth = 1

class MymovieSerializer(serializers.ModelSerializer):
    # ratings = RatingSerializer(many=True, read_only=True)
    ratings = serializers.CharField(source='movie.ratings', read_only=True)
    movie_genre = serializers.CharField(source='movie.genres', read_only=True)

    class Meta:
        model = Mymovie
        fields = '__all__'
        read_only_fields = ('movie', 'user')
        depth = 1


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    rating_count = serializers.IntegerField(source='ratings.count', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

# class MovieListSerializer(serializers.ModelSerializer):
#     ratings = RatingSerializer(many=True, read_only=True)
#     rating_count = serializers.IntegerField(source='ratings.count', read_only=True)

#     class Meta:
#         model = Movie
#         fields = '__all__'

class RecommandSerializer(serializers.ModelSerializer):
    pass