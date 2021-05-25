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
    ratings = RatingSerializer(many=True, read_only=True)
    # ratings = serializers.CharField(source='movie.ratings', read_only=True)
    rating_count = serializers.IntegerField(source='movie.ratings.count', read_only=True)
    # rating_average = serializers.SerializerMethodField('score_average')

    # def score_average(self, mov):
    #     cnt = mov.movie.ratings.count()
    #     score_sum = 0
    #     if cnt:
    #         for rating in mov.ratings.all():
    #             score_sum += rating.score
    #         rst = round(score_sum/cnt, 2)
    #     else:
    #         rst = 0
    #     return rst

    class Meta:
        model = Mymovie
        fields = '__all__'
        read_only_fields = ('movie', 'user')
        depth = 1


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    rating_count = serializers.IntegerField(source='ratings.count', read_only=True)
    rating_average = serializers.SerializerMethodField('score_average')

    def score_average(self, mov):
        cnt = mov.ratings.count()
        score_sum = 0
        if cnt:
            for rating in mov.ratings.all():
                score_sum += rating.score
            rst = round(score_sum/cnt, 2)
        else:
            rst = 0
        return rst

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