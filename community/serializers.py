from django.db.models import fields
from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format="%y년%m월%d일 %H시 %M분")

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article',)


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    created_at = serializers.DateTimeField(format="%y년%m월%d일 %H시 %M분")

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)
        depth = 1

class ArticleListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)
