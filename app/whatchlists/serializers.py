from rest_framework import serializers

from whatchlists.models import Movie, Series, Season, Episode


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'get_runtime', 'released', 'genres', 'imdb_rating']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'released', 'episode_numb', 'runtime', 'plot', 'imdb_rating']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ['season_numb', 'total_episodes', 'episodes']


class SeriesSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ['title', 'year', 'released', 'genres', 'plot', 'imdb_rating', 'total_seasons', "seasons"]
