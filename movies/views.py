from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Movie, Mymovie, Rating
from .serializers import  MovieSerializer, RatingSerializer, MymovieSerializer
from .tmdb import get_movie_json, genres, PAGE_NUM


# Create your views here.
@api_view(['GET'])
def get_movies(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        srz = MovieSerializer(movies, many=True)
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
            movie_parsed['movie_id'] = movie['id']
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

@api_view(['POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def rating(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    # print(movie_id)
    srz = RatingSerializer(data=request.data)
    if srz.is_valid(raise_exception=True):
        srz.save(movie=movie, user=request.user)
        return Response(srz.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def update_rating(request, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)

    # 1. 해당 rating작성한 유저가 아닌 경우 수정하거나 삭제하지 못하게
    if not request.user.ratings.filter(pk=rating_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        rating.delete()
        return Response({ 'id': rating_pk }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])  
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated]) 
def get_mymovie(request):
    if request.method == 'GET':
        serializer = MymovieSerializer(request.user.mymovies, many=True)
        return Response(serializer.data)

@api_view(['POST'])  
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated]) 
def create_mymovie(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, movie_id=movie_id)
        serializer = MymovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])  
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated]) 
def delete_mymovie(request, mymovie_pk):
    mymovie = get_object_or_404(Mymovie, pk=mymovie_pk)
    if not request.user.mymovies.filter(pk=mymovie_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'DELETE':
        mymovie.delete()
        return Response({ 'id': mymovie_pk }, status=status.HTTP_204_NO_CONTENT)
    

def recommand(request):
    # 유저가 4점 이상 평점을 준 영화와 찜목록에 넣은 영화 id를 조회해서
    # mymovie 조회
    mymovie = get_list_or_404(Mymovie, user_id=request.user)
    # 장르별로 딕셔너리에 점수를 부여 가장높은 점수를 받은 장르의 영화를 평점순으로 추천. 
    pass