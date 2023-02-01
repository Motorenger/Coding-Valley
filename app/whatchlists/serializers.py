from rest_framework import serializers

from whatchlists.models import Movie, Series


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'get_runtime', 'released', 'genres']
        depth = 1


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'title', 'year', 'released', 'genres', 'plot', 'total_seasons', 'imdb_id']
