import os

import pytest
import requests

from watchlists.services.db_saving import save_movie, save_series
from watchlists.models import Movie, Series


pytestmark = pytest.mark.django_db
BASE_OMDB_URL = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}"


def test_save_movie(mocker):
    # given
    omdb_id = "tt1515091"
    movie_data = requests.get(BASE_OMDB_URL + f"&i={omdb_id}").json()
    mocker.patch("watchlists.services.omdb_requests.get_omdb_by_omdbid", return_value=movie_data)
    # when
    test_data = save_movie(omdb_id)
    # then
    assert Movie.objects.count() == 1, "The db must have one movie"
    assert test_data.title == movie_data.get('Title'), "The title of test data is not equal to the title of movie data"
    assert test_data.genres == movie_data.get('Genre'), "The genres of test data is not equal to the genres of movie data"


def test_save_series(mocker):
    # given
    omdb_id = "tt0944947"
    series_data = requests.get(BASE_OMDB_URL + f"&i={omdb_id}").json()
    mocker.patch("watchlists.services.omdb_requests.get_omdb_by_omdbid", return_value=series_data)
    # when
    test_data = save_series(omdb_id)
    # then
    assert Series.objects.count() == 1, "The db must have one series"
    assert test_data.title == series_data.get('Title'), "The title of test data is not equal to the title of movie data"
    assert test_data.genres == series_data.get('Genre'), "The genres of test data is not equal to the genres of movie data"
