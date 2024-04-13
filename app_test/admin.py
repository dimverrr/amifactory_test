from django.contrib import admin
from .models import Movie, Genre, Person

# Register your models here.

models = [Movie, Genre, Person]

admin.site.register(models)
