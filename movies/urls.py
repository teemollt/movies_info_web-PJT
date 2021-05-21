from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_movies),
    path('updatelist/', views.update_movies)
]
