import os

import requests


def get_omdb_by_search(search: str) -> dict:
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&s={search}").json()
    return data


def get_omdb_by_omdbid(omdb_id: str):
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    return data
