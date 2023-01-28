from rest_framework import serializers

from whatchlists.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'get_runtime', 'released', 'genres']
        depth = 1
