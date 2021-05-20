from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie
from .serializers import  MovieSerializer, MovieListSerializer
from .tmdb import get_movie_json


# Create your views here.
@api_view(['GET', 'POST'])
def get_movies(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        srz = MovieListSerializer(movies, many=True)
        return Response(srz.data)

    elif request.method == 'POST':
        movie_json = get_movie_json()
        # print(movie_json)

        for movie in movie_json:
            # data parse
            posterpath = movie['poster_path']
            movie_parsed = {}
            movie_parsed['title'] = movie['title']
            movie_parsed['overview'] = movie['overview']
            movie_parsed['poster_path'] = f'https://image.tmdb.org/t/p/original{posterpath}'
            movie_parsed['release_date'] = movie['release_date']
            # serializer : save json type data to sqlite
            srz = MovieSerializer(data=movie_parsed)
            if srz.is_valid(raise_exception=True):
                srz.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)