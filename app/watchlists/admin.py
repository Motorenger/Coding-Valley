from django.contrib import admin

from watchlists.models import Media, Season, Episode


class SeasonInline(admin.TabularInline):
    model = Media.seasons.through


class EpisodeInline(admin.TabularInline):
    model = Season.episodes.through


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'released', 'episode_numb', 'imdb_rating')
    list_filter = ('imdb_rating', 'episode_numb')
    search_fields = ('title',)


@admin.register(Season)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('season_numb', 'total_episodes')
    list_filter = ('season_numb',)
    exclude = ('episodes',)
    inlines = [
        EpisodeInline,
    ]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'released', 'imdb_id', 'imdb_rating')
    list_filter = ('imdb_rating', 'media_type')
    search_fields = ('title',)
    exclude = ('seasons',)
    inlines = [
        SeasonInline,
    ]
