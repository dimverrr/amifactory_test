from djantic import ModelSchema
from enum import Enum

from .models import Movie, Genre, Person


class MovieRateEnum(str, Enum):
    G = ("G",)
    PG = ("PG",)
    PG_13 = ("PG-13",)
    R = ("R",)
    NC_17 = "NC-17"


class GenreSchema(ModelSchema):
    class Config:
        model = Genre


class GenreResponseSchema(ModelSchema):
    class Config:
        model = Genre
        exclude = ["created_at", "updated_at", "movie_set"]


class MovieSchema(ModelSchema):
    class Config:
        model = Movie


class MovieResponseSchema(ModelSchema):
    class Config:
        model = Movie
        exclude = ["created_at", "updated_at"]

    mpa_rating: MovieRateEnum


class PersonSchema(ModelSchema):
    class Config:
        model = Person
