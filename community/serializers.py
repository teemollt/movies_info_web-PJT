from django.db.models import fields
from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article',)


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)

class ArticleListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'comments_count',)
