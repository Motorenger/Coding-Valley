from rest_framework import serializers

from whatchlists.models import Movie, Series, Season, Episode


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'get_runtime', 'released', 'genres', 'poster', 'imdb_rating']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'released', 'episode_numb', 'runtime', 'plot', 'poster', 'imdb_rating']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = ['season_numb', 'total_episodes', 'episodes']

    def get_episodes(self, instance):
        imdb_rating = self.context["imdb_rating"]
        if imdb_rating is not None:
            episodes = instance.episodes.filter(imdb_rating__gte=imdb_rating)
        else:
            episodes = instance.episodes.all()
        return EpisodeSerializer(episodes, many=True).data


class SeriesSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ['title', 'year', 'released', 'genres', 'plot', 'imdb_rating', 'total_seasons', "poster", "seasons"]
