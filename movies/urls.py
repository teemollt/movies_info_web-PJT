from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_movies),
    path('updatelist/', views.update_movies),
    path('<int:movie_pk>/rating/', views.rating),
    path('rating/<int:rating_pk>/update/', views.update_rating),
    path('mymovies/', views.get_mymovie),
    path('<int:movie_pk>/create_mymovie/', views.create_mymovie),
    path('<int:mymovie_pk>/delete_mymovie/', views.delete_mymovie),
]
