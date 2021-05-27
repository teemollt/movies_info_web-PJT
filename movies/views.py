from django.shortcuts import render, get_list_or_404, get_object_or_404
from collections import OrderedDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Movie, Mymovie, Rating
from .serializers import  MovieSerializer, RatingSerializer, MymovieSerializer
from .tmdb import get_movie_json, genres, PAGE_NUM

# def most_cnt(val):
#     assert isinstance(val, list)
#     if len(val) == 0: return None
#     return Counter(val).most_common(n=1)[0][0]

# Create your views here.
@api_view(['GET'])
def get_movies(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        srz = MovieSerializer(movies, many=True)
        return Response(srz.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        srz = MovieSerializer(movie)
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
            remove_char = "[]\'"
            genres_char = ', '.join(x for x in genre_text if x not in remove_char)
            movie_parsed['genres'] = f'{genres_char}'
            # serializer : save json type data to sqlite
            srz = MovieSerializer(data=movie_parsed)
            if srz.is_valid(raise_exception=True):
                srz.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED, data=f'{PAGE_NUM} 페이지 추가')

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def rating(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    srz = RatingSerializer(data=request.data)
    if srz.is_valid(raise_exception=True):
        srz.save(movie=movie, user=request.user)
        if srz.data['score'] >= 4:
            genres_raw = srz.data['movie_genre']
            remove_char = "[]\' "
            genres_char = ''.join(x for x in genres_raw if x not in remove_char)
            genres_list= genres_char.split(',')
            print(genres_list)
            # print(genres_list)
            # list_g = ['action','adventure','animation','comedy','crime','drama','family','fantasy','history','horror','music','mystery','romance','SF','TV_movie','thriller','war','western']

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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def get_mymovie(request):
    if request.method == 'GET':
        serializer = MymovieSerializer(request.user.mymovies, many=True)
        return Response(serializer.data)

@api_view(['POST'])  
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def create_mymovie(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MymovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])  
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def delete_mymovie(request, mymovie_pk):
    mymovie = get_object_or_404(Mymovie, pk=mymovie_pk)
    if not request.user.mymovies.filter(pk=mymovie_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'DELETE':
        mymovie.delete()
        return Response({ 'id': mymovie_pk }, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])  
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def get_recommand(request):
    # 해당 유저의 선호 장르들 개수 세서 젤 많은거 
    # 찜한 영화들 장르 가져오기
    mymovies = Mymovie.objects.filter(user=request.user.id)
    srz = MymovieSerializer(mymovies, many=True)
    mymovies_id_list = []
    genre_cnt_list = []
    for i in range(len(srz.data)):
        genre_raw = dict(OrderedDict(dict(OrderedDict(srz.data[i]))['movie']))['genres']
        mymovies_id_list.append(dict(OrderedDict(dict(OrderedDict(srz.data[i]))['movie']))['id'])
        genre = genre_raw.replace(" ","")
        g_list = genre.split(',')
        for j in range(len(g_list)):
            genre_cnt_list.append(g_list[j])  
    # genre_cnt_list => 찜한 영화의 장르들 전부 넣은 리스트          
    # 이제 4점 이상 평점준 영화 장르들 가져오기
    ratings = Rating.objects.filter(user=request.user.id)
    srz2 = RatingSerializer(ratings, many=True)
    # print(srz2.data)
    # genre_raw2 = dict(OrderedDict(srz2.data[0]))['movie_genre']
    # print(genre_raw2)
    for i in range(len(srz2.data)):
        # 내가 평점준 영화(점수 관계없이) id들 담아두기 ( 나중에 추천할때 거르기위해서)
        mymovies_id_list.append(dict(OrderedDict(srz2.data[i]))['id'])
        # 4 초과로 점수 준 영화의 장르만 뽑자
        if (dict(OrderedDict(srz2.data[i]))['score']) > 4:
            genre_raw2 = dict(OrderedDict(srz2.data[i]))['movie_genre']
            genre2 = genre_raw2.replace(" ","")
            g_list2 = genre2.split(',')
            for j in range(len(g_list2)):
                genre_cnt_list.append(g_list2[j])  
    # print(genre_cnt_list)
    # 카운트 하기
    genre_name = ['액션','모험','애니메이션','코미디','범죄','다큐멘터리','드라마','가족','판타지',
        '역사','공포','음악','미스터리','로맨스','SF','TV 영화','스릴러','전쟁','서부']
    # g_tmp = ""
    max_cnt = 0
    # for i in range(len(genre_cnt_list)):
    #     g_tmp = genre_cnt_list[i]
    #     cnt_tmp = 0
    #     for j in range(len(genre_cnt_list)):
    #         if g_tmp == genre_cnt_list[j]:
    #             cnt_tmp += 1
    #     if cnt_tmp >= max_cnt:
    #         max_cnt = cnt_tmp
    #         favorite_genre = g_tmp
    # print(favorite_genre)
    for gen in genre_name:
        cnt = genre_cnt_list.count(gen)
        if cnt >= max_cnt:
            max_cnt = cnt
            favorite_genre = gen
    print(favorite_genre)
    movies = get_list_or_404(Movie)
    movies_srz = MovieSerializer(movies, many=True)
    # movies_dic = dict(OrderedDict(movies_srz.data))
    # print(mymovies_id_list)
    recommand_movies = []
    for i in range(len(movies_srz.data)):
        movie = dict(OrderedDict(movies_srz.data[i]))
        # 선호장르가 포함되면서 이미 찜했거나 점수준 영화는 빼기
        if favorite_genre in movie['genres'] and movie['id'] not in mymovies_id_list:
            # print(dict(OrderedDict(movies_srz.data[i]))['title'])
            recommand_movies.append(movie)
    return Response(recommand_movies)