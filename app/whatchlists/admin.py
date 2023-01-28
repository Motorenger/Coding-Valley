from django.contrib import admin

from whatchlists.models import Genre, Movie


class GenreInline(admin.TabularInline):
    model = Movie.genres.through


class MovieAdmin(admin.ModelAdmin):
    exclude = ('genres',)
    inlines = [
        GenreInline,
    ]


admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
