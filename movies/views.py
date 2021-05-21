from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie
from .serializers import  MovieSerializer, MovieListSerializer
from .tmdb import get_movie_json, genres, PAGE_NUM


# Create your views here.
@api_view(['GET'])
def get_movies(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        srz = MovieListSerializer(movies, many=True)
        return Response(srz.data)
  
@api_view(['POST'])
def update_movies(request):
    if request.method == 'POST':
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
            movie_parsed['popularity'] = int(movie['popularity'] * 1000)
            # 장르id(리스트 내 숫자 id 형태)
            genre_id = movie['genre_ids']
            genre_text = []
            for g in genre_id:
                genre_text.append(genres[f'{g}'])
            # print(genre_text)
            # print(genre_id)
            movie_parsed['genres'] = f'{genre_text}'
            
            # serializer : save json type data to sqlite
            srz = MovieSerializer(data=movie_parsed)
            if srz.is_valid(raise_exception=True):
                srz.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED, data=f'{PAGE_NUM} 페이지 추가')