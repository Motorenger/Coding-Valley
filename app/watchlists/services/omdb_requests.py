import os

import requests

from django.http import Http404


def get_omdb_by_search(search: str, page, year) -> dict:
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&s={search}&page={page}&y={year}").json()
    return data


def get_omdb_by_omdbid(omdb_id: str, session=None):
    if session:
        data = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    else:
        data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    if (data['Response'] == "True"):
        return data
    raise Http404


def get_season_by_omdbid(series_omdb_id: str, season_numb: int, session) -> dict:
    data = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={series_omdb_id}&Season={season_numb}").json()
    if (data['Response'] == "True"):
        return data
    raise Http404


def get_episode_by_omdbid(episode_omdb_id: str, session) -> dict:
    data = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={episode_omdb_id}").json()
    if (data['Response'] == "True"):
        return data
    raise Http404
