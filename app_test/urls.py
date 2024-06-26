from . import views
from django.urls import path

urlpatterns = [
    path("movies/", views.get_all_movies, name="get all movies"),
    path("movies/<int:movie_id>/", views.get_one_movie, name="get all movies"),
    path("genres/", views.get_genres, name="get all genres"),
]
