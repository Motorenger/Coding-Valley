from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


from whatchlists.models import Movie
from whatchlists.serializers import MovieSerializer
from whatchlists.utills import get_omdb_by_search, get_omdb_by_omdbid, save_to_db_or_get


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
    # getting data from omdb
    omdb_id = request.query_params['omdb_id']
    search_results = get_omdb_by_omdbid(omdb_id)

    data = save_to_db_or_get(search_results)
    serializer = MovieSerializer(data)

    return Response(serializer.data)
