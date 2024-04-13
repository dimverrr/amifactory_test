from django.http import JsonResponse
from .models import Movie, Genre
from django.core.paginator import Paginator


# Create your views here.
def get_all_movies(request):
    movies = Movie.objects.all().order_by("id")

    paginator = Paginator(movies, 1)

    genre = request.GET.get("genre")
    if genre:
        if not Genre.objects.filter(id=genre):
            return JsonResponse({"error": ["genre__invalid"]}, status=400)
        movies = movies.exclude(genres__id=genre)

    src = request.GET.get("src")
    if src:
        if len(src) < 2 or len(src) > 14:
            return JsonResponse({"error": ["src__invalid"]}, status=400)
        movies = movies.filter(title__icontains=src)

    page = request.GET.get("page")
    if page:
        if paginator.num_pages < int(page):
            return JsonResponse({"error": ["page__out_of_bounds"]}, status=400)
        page_obj = paginator.get_page(page)
        movies = page_obj.object_list

    movie_data = []
    for movie in movies:
        genres_data = [
            {"id": genre.id, "title": genre.title} for genre in movie.genres.all()
        ]
        directors_data = [
            {
                "id": director.id,
                "first_name": director.first_name,
                "last_name": director.last_name,
            }
            for director in movie.directors.all()
        ]
        writers_data = [
            {
                "id": writer.id,
                "first_name": writer.first_name,
                "last_name": writer.last_name,
            }
            for writer in movie.writers.all()
        ]
        stars_data = [
            {"id": star.id, "first_name": star.first_name, "last_name": star.last_name}
            for star in movie.stars.all()
        ]

        movie_data.append(
            {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_year": movie.release_year.year,
                "mpa_rating": movie.mpa_rating,
                "imdb_rating": movie.imdb_rating,
                "duration": movie.duration,
                "poster": movie.poster.url,
                "bg_picture": movie.bg_picture.url,
                "genres": genres_data,
                "directors": directors_data,
                "writers": writers_data,
                "stars": stars_data,
            }
        )
    response_data = {
        "total": len(movie_data),
        "pages": paginator.num_pages,
        "results": movie_data,
    }
    response = JsonResponse(response_data, safe=False, status=200)
    return response


def get_one_movie(request, movie_id):
    movie = Movie.objects.filter(id=movie_id).first()
    movie_data = []
    genres_data = [
        {"id": genre.id, "title": genre.title} for genre in movie.genres.all()
    ]
    directors_data = [
        {
            "id": director.id,
            "first_name": director.first_name,
            "last_name": director.last_name,
        }
        for director in movie.directors.all()
    ]
    writers_data = [
        {
            "id": writer.id,
            "first_name": writer.first_name,
            "last_name": writer.last_name,
        }
        for writer in movie.writers.all()
    ]
    stars_data = [
        {"id": star.id, "first_name": star.first_name, "last_name": star.last_name}
        for star in movie.stars.all()
    ]

    movie_data.append(
        {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_year": movie.release_year.year,
            "mpa_rating": movie.mpa_rating,
            "imdb_rating": movie.imdb_rating,
            "duration": movie.duration,
            "poster": movie.poster.url,
            "bg_picture": movie.bg_picture.url,
            "genres": genres_data,
            "directors": directors_data,
            "writers": writers_data,
            "stars": stars_data,
        }
    )
    response = JsonResponse(movie_data, safe=False, status=200)
    return response


def get_genres(request):
    all_genres = list(Genre.objects.values("id", "title"))
    response = JsonResponse(all_genres, safe=False, status=200)
    return response


def custom_500(request):
    return JsonResponse({"error": ["internal"]}, status=500)
