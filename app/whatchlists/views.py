from rest_framework import viewsets

from whatchlists.models import Movie
from whatchlists.serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
