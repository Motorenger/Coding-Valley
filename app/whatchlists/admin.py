from django.contrib import admin

from whatchlists.models import (Genre, Movie,
                                Series, Season,
                                Episode
                                )


class GenreInline(admin.TabularInline):
    model = Movie.genres.through


class MovieAdmin(admin.ModelAdmin):
    exclude = ('genres',)
    inlines = [
        GenreInline,
    ]


class SeasonInline(admin.TabularInline):
    model = Season


class SeriesAdmin(admin.ModelAdmin):
    inlines = [
        SeasonInline,
    ]


class EpisodeInline(admin.TabularInline):
    model = Episode


class SeasonAdmin(admin.ModelAdmin):
    inlines = [
        EpisodeInline,
    ]


admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Episode)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Series, SeriesAdmin)
