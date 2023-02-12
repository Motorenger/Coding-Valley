import os

import pytest
import requests
from django.urls import reverse

from watchlists.models import Series, Movie


pytestmark = pytest.mark.django_db
BASE_OMDB_URL = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}"


def test_get_with_no_query_params(api_client):
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"))
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_type_query_param(api_client):
    # given
    type = "series"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"type": type})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_imdb_id_query_param(api_client):
    # given
    imdb_id = "tt0944947"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_incorrect_type_query_params(api_client):
    # given
    imdb_id = "tt0944947"
    type = "incorrect_type"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_incorrect_imdb_id_and_type_query_params(api_client):
    # given
    imdb_id = "incorrect_imdb_id"
    type = "series"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_type_query_params_for_series(api_client):
    # given
    imdb_id = "tt0944947"
    type = "series"
    expected_response = requests.get(BASE_OMDB_URL + f"&i={imdb_id}")
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type})
    # then
    assert test_response.json().get('title') == expected_response.json().get('Title'), "The title of test response is not equal to the title of expected response"
    assert test_response.json().get('genres') == expected_response.json().get('Genre'), "The genres of test response is not equal to the genres of expected response"
    assert Series.objects.count() == 1, "The data has not been saved in db"


def test_get_with_imdb_id_and_type_query_params_for_movie(api_client):
    # given
    imdb_id = "tt1515091"
    type = "movie"
    expected_response = requests.get(BASE_OMDB_URL + f"&i={imdb_id}")
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type})
    # then
    assert test_response.json().get('title') == expected_response.json().get('Title'), "The title of test response is not equal to the title of expected response"
    assert test_response.json().get('genres') == expected_response.json().get('Genre'), "The genres of test response is not equal to the genres of expected response"
    assert Movie.objects.count() == 1, "The data has not been saved in db"


def test_get_with_imdb_id_and_type_and_incorrect_imdb_rating_query_params_for_series(api_client):
    # given
    imdb_id = "tt0944947"
    type = "series"
    imdb_rating = "incorrect_rating"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type, "imdb_rating": imdb_rating})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_type_and_imdb_rating_query_params_for_series(api_client):
    # given
    imdb_id = "tt0944947"
    type = "series"
    imdb_rating = "9.3"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_by_omdbid"), {"imdb_id": imdb_id, "type": type, "imdb_rating": imdb_rating})
    # then
    for season in test_response.json().get('seasons'):
        for episode in season.get('episodes'):
            assert episode.get('imdb_rating') >= float(imdb_rating)
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_post(api_client):
    # when
    test_response = api_client.post(reverse("watchlists_app:get_by_omdbid"), {})
    # then
    assert test_response.status_code == 405, "Status code of response must be 405"
