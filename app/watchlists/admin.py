from django.contrib import admin

from watchlists.models import Media, Season, Episode


class SeasonInline(admin.TabularInline):
    model = Media.seasons.through


class MediaAdmin(admin.ModelAdmin):
    exclude = ('seasons',)
    inlines = [
        SeasonInline,
    ]


admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Media, MediaAdmin)
