from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.
MPA_RATING_CHOICES = [
    ("G", "G"),
    ("PG", "PG"),
    ("PG-13", "PG-13"),
    ("R", "R"),
    ("NC-17", "NC-17"),
]
PERSON_TYPE_CHOICES = [
    ("director", "Director"),
    ("writer", "Writer"),
    ("actor", "Actor"),
]


def validate_release_year(value):
    if not isinstance(value, int) or value < 1888 or value > datetime.now().year:
        raise ValidationError(
            "Invalid release year. Please enter a valid year between 1800 and the current year."
        )


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.title


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.CharField(
        choices=PERSON_TYPE_CHOICES, max_length=8, default=PERSON_TYPE_CHOICES[0][0]
    )

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=5000)
    poster = models.ImageField()
    bg_picture = models.ImageField()
    release_year = models.IntegerField(validators=[validate_release_year])
    mpa_rating = models.CharField(
        choices=MPA_RATING_CHOICES, max_length=5, default=MPA_RATING_CHOICES[0][0]
    )
    imdb_rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(
        Person,
        related_name="directed_movies",
        limit_choices_to={"types__contains": "director"},
    )
    writers = models.ManyToManyField(
        Person,
        related_name="written_movies",
        limit_choices_to={"types__contains": "writer"},
    )
    stars = models.ManyToManyField(
        Person,
        related_name="starred_movies",
        limit_choices_to={"types__contains": "actor"},
    )

    def __str__(self) -> str:
        return self.title
