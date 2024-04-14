from django.http import JsonResponse
from .models import Movie, Genre
from django.core.paginator import Paginator
from .schemas import MovieResponseSchema, GenreResponseSchema
import logging


def get_all_movies(request):
    try:
        movies = Movie.objects.all().order_by("id")
        paginator = Paginator(movies, 10)

        genre = request.GET.get("genre")
        if genre:
            if not Genre.objects.filter(id=genre):
                return JsonResponse({"error": ["genre__invalid"]}, status=400)
            movies = movies.filter(genres__id=genre)

        src = request.GET.get("src")
        if src:
            if len(src) < 2 or len(src) > 14:
                return JsonResponse({"error": ["src__invalid"]}, status=400)
            movies = movies.filter(title__icontains=src)

        page = request.GET.get("page")
        if page:
            try:
                page = int(page)
            except ValueError:
                return JsonResponse({"error": ["page__invalid"]}, status=400)

            if paginator.num_pages < page or page < 0:
                return JsonResponse({"error": ["page__out_of_bounds"]}, status=400)

            page_obj = paginator.get_page(page)
            movies = page_obj.object_list

        movie_data = []
        for movie in movies:
            movie_schema = MovieResponseSchema.from_django(movie)
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
                {
                    "id": star.id,
                    "first_name": star.first_name,
                    "last_name": star.last_name,
                }
                for star in movie.stars.all()
            ]

            movie_dict = movie_schema.dict()
            movie_dict.update(
                {
                    "genres": genres_data,
                    "directors": directors_data,
                    "writers": writers_data,
                    "stars": stars_data,
                }
            )
            movie_data.append(movie_dict)

        response_data = {
            "total": len(movie_data),
            "pages": paginator.num_pages,
            "results": movie_data,
        }
        response = JsonResponse(response_data, safe=False, status=200)
        return response
    except Exception as e:
        logging.error(e)
        return JsonResponse({"error": ["internal"]}, status=500)


def get_one_movie(request, movie_id):
    try:
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            return JsonResponse({"error": ["movie__not_found"]}, status=404)

        movie_schema = MovieResponseSchema.from_django(movie)
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

        movie_dict = movie_schema.dict()
        movie_dict.update(
            {
                "genres": genres_data,
                "directors": directors_data,
                "writers": writers_data,
                "stars": stars_data,
            }
        )

        response = JsonResponse(movie_dict, status=200)
        return response

    except Exception as e:
        logging.error(e)
        return JsonResponse({"error": ["internal"]}, status=500)


def get_genres(request):
    try:
        all_genres = Genre.objects.all()
        data = []
        for genre in all_genres:
            genre_schema = GenreResponseSchema.from_django(genre)
            data.append(genre_schema.dict())
        response = JsonResponse(data, safe=False, status=200)
        return response
    except Exception as e:
        logging.error(e)
        return JsonResponse({"error": ["internal"]}, status=500)
