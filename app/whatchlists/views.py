from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from whatchlists.models import Movie
from whatchlists.serializers import MovieSerializer
from whatchlists.utills import get_omdb_by_search, get_omdb_by_omdbid


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


@api_view()
def search_by_search_test_view(request):
    search = request.query_params['search']
    search_results = get_omdb_by_search(search)

    return Response(search_results)


@api_view()
def search_by_omdbid_test_view(request):
    omdb_id = request.query_params['omdb_id']
    search_results = get_omdb_by_omdbid(omdb_id)

    return Response(search_results)
