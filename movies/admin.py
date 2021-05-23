from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_display_links = ['id', 'title']
    search_fields = ['title', ]
