import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_get_with_no_query_params(api_client):
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"))
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_imdb_id_query_params(api_client):
    # given
    imdb_id = "tt1234567"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"imdb_id": imdb_id})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_season_query_params(api_client):
    # given
    season = 1
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"season": season})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_incorrect_imdb_id_and_season_query_params(api_client):
    # given
    imdb_id = "incorrect_imdb_id"
    season = 1
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"imdb_id": imdb_id, "season": season})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_incorrect_season_query_params(api_client):
    # given
    imdb_id = "tt1234567"
    season = "incorrect_season_number"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"imdb_id": imdb_id, "season": season})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_season_query_params(api_client, series_tt1234567):
    # given
    imdb_id = "tt1234567"
    season = 1
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"imdb_id": imdb_id, "season": season})
    # then
    assert test_response.json()['season_numb'] == season, "The season number of test response is not equal to the given season number"
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_get_with_imdb_id_and_season_and_incorrect_imdb_rating_query_params(api_client):
    # given
    imdb_id = "tt1234567"
    season = 1
    imdb_rating = "incorrect_rating"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"imdb_id": imdb_id, "season": season, "imdb_rating": imdb_rating})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_imdb_id_and_season_and_imdb_rating_query_params(api_client, series_tt1234567):
    # given
    imdb_id = "tt1234567"
    season = 1
    imdb_rating = "9.3"
    # when
    test_response = api_client.get(reverse("watchlists_app:get_season_by_omdbid"), {"imdb_id": imdb_id, "season": season, "imdb_rating": imdb_rating})
    # then
    for episode in test_response.json().get('episodes'):
        assert episode.get('imdb_rating') >= float(imdb_rating)
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_post(api_client):
    # when
    test_response = api_client.post(reverse("watchlists_app:get_season_by_omdbid"), {})
    # then
    assert test_response.status_code == 405, "Status code of response must be 405"
