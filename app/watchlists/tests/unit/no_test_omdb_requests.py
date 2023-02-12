import os

import requests

from watchlists.services.omdb_requests import (
    get_omdb_by_search, get_omdb_by_omdbid,
    get_season_by_omdbid, get_episode_by_omdbid
)


BASE_OMDB_URL = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}"


def test_get_omdb_by_search_with_correct_data():
    # given
    search = "Game"
    year = 2016
    page = 4
    expected_data = requests.get(BASE_OMDB_URL + f"&s={search}&y={year}&page={page}").json()
    # when
    test_data = get_omdb_by_search(search, page, year)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_omdb_by_search_with_incorrect_data():
    # given
    search = "incorrect_search"
    year = "incorrect_year"
    page = "incorrect_page"
    expected_data = requests.get(BASE_OMDB_URL + f"&s={search}&y={year}&page={page}").json()
    # when
    test_data = get_omdb_by_search(search, page, year)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_omdb_by_omdbid_with_correct_data():
    # given
    omdb_id = "tt1515091"
    session = requests.Session()
    expected_data = requests.get(BASE_OMDB_URL + f"&i={omdb_id}").json()
    # when
    test_data = get_omdb_by_omdbid(omdb_id, session)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_omdb_by_omdbid_with_incorrect_data():
    # given
    omdb_id = "incorrect_omdb_id"
    expected_data = requests.get(BASE_OMDB_URL + f"&i={omdb_id}").json()
    # when
    test_data = get_omdb_by_omdbid(omdb_id)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_omdb_by_omdbid_with_correct_data_and_without_session():
    # given
    omdb_id = "tt1515091"
    expected_data = requests.get(BASE_OMDB_URL + f"&i={omdb_id}").json()
    # when
    test_data = get_omdb_by_omdbid(omdb_id)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_season_by_omdbid_with_correct_data():
    # given
    series_omdb_id = "tt0944947"
    season_numb = 1
    session = requests.Session()
    expected_data = session.get(BASE_OMDB_URL + f"&i={series_omdb_id}&Season={season_numb}").json()
    # when
    test_data = get_season_by_omdbid(series_omdb_id, season_numb, session)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_season_by_omdbid_with_incorrect_data():
    # given
    series_omdb_id = "incorrect_series_omdb_id"
    season_numb = "incorrect_season_numb"
    session = requests.Session()
    expected_data = session.get(BASE_OMDB_URL + f"&i={series_omdb_id}&Season={season_numb}").json()
    # when
    test_data = get_season_by_omdbid(series_omdb_id, season_numb, session)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_episode_by_omdbid_with_correct_data():
    # given
    episode_omdb_id = "tt1480055"
    session = requests.Session()
    expected_data = session.get(BASE_OMDB_URL + f"&i={episode_omdb_id}").json()
    # when
    test_data = get_episode_by_omdbid(episode_omdb_id, session)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"


def test_get_episode_by_omdbid_with_incorrect_data():
    # given
    episode_omdb_id = "incorrect_episode_omdb_id"
    session = requests.Session()
    expected_data = session.get(BASE_OMDB_URL + f"&i={episode_omdb_id}").json()
    # when
    test_data = get_episode_by_omdbid(episode_omdb_id, session)
    # then
    assert test_data == expected_data, "The test data is not equal to expected data"
