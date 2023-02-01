from django.contrib import admin

from whatchlists.models import (Movie,
                                Series, Season,
                                Episode
                                )


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


admin.site.register(Movie)
admin.site.register(Episode)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Series, SeriesAdmin)
