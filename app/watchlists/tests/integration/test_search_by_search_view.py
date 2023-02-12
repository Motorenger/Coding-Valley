import os

import requests
from django.urls import reverse


BASE_OMDB_URL = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}"


def test_get_with_no_query_params(api_client):
    # when
    test_response = api_client.get(reverse("watchlists_app:search"))
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_only_search_query_param(api_client):
    # given
    search = "Game of Thrones"
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}")
    # when
    test_response = api_client.get(reverse("watchlists_app:search"), {"search": search})
    # then
    assert test_response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_get_with_search_and_year_query_params(api_client):
    # given
    search = "Game of Thrones"
    year = 2016
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}&y={year}")
    # when
    test_response = api_client.get(reverse("watchlists_app:search"), {"search": search, "year": year})
    # then
    assert test_response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_get_with_search_and_page_query_params(api_client):
    # given
    search = "Game of Thrones"
    page = 4
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}&page={page}")
    # when
    test_response = api_client.get(reverse("watchlists_app:search"), {"search": search, "page": page})
    # then
    assert test_response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_get_with_year_and_page_query_params(api_client):
    # given
    year = 2016
    page = 4
    # when
    test_response = api_client.get(reverse("watchlists_app:search"), {"year": year, "page": page})
    # then
    assert test_response.status_code == 404, "Status code of response must be 404"


def test_get_with_search_and_year_and_page_query_params(api_client):
    # given
    search = "Game"
    year = 2016
    page = 4
    expected_response = requests.get(BASE_OMDB_URL + f"&s={search}&y={year}&page={page}")
    # when
    test_response = api_client.get(reverse("watchlists_app:search"), {"search": search, "year": year, "page": page})
    # then
    assert test_response.json() == expected_response.json(), "The test response is not equal to expected response"
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_post(api_client):
    # when
    test_response = api_client.post(reverse("watchlists_app:search"), {})
    # then
    assert test_response.status_code == 405, "Status code of response must be 405"
