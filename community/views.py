from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Article, Comment
from .serializers import  ArticleSerializer, CommentSerializer

@api_view(['GET'])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        srz = ArticleSerializer(articles, many=True)
        return Response(srz.data)

@api_view(['POST'])
def article_create(request, article_pk):
    if request.method == 'GET':
        srz = ArticleSerializer(request.user.articles)
    elif request.method == 'POST':
        srz = ArticleSerializer(data=request.data)
        if srz.is_valid(raise_exception=True):
            srz.save(user=request.user)
            return Response(srz.data, status=status.HTTP_201_CREATED)

