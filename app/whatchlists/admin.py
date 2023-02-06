from django.contrib import admin

from whatchlists.models import Media, Season, Episode


class EpisodeInline(admin.TabularInline):
    model = Episode


class SeasonAdmin(admin.ModelAdmin):
    inlines = [
        EpisodeInline,
    ]


admin.site.register(Episode)
admin.site.register(Season, SeasonAdmin)


admin.site.register(Media)
