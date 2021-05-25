from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list),
    path('article_create/', views.article_create),
    path('articles/<int:article_pk>/', views.article_change),
    path('comments/', views.comment_list),
    path('articles/<int:article_pk>/comment/', views.create_comment),
    path('comments/<int:comment_pk>/', views.comment_change),
]