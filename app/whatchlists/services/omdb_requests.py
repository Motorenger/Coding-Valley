import os

import requests


def get_omdb_by_search(search: str) -> dict:
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&s={search}").json()
    return data


def get_omdb_by_omdbid(omdb_id: str, session=None):
    if session:
        data = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    else:
        data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    return data


def get_season_by_omdbid(series_omdb_id: str, season_numb: int, session) -> dict:
    season = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={series_omdb_id}&Season={season_numb}").json()
    return season


def get_episode_by_omdbid(episode_omdb_id: str, session) -> dict:
    episode = session.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={episode_omdb_id}").json()
    return episode
