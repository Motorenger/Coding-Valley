from rest_framework import viewsets

from movies.models import Movie
from movies.api.serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
