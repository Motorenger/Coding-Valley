import datetime
import asyncio
import os

import aiohttp

from celery import shared_task

from watchlists.services import omdb_requests as req
from watchlists.models import Series, Season, Episode


def get_seasons(session, series_data):
    tasks = []
    for season_number in range(1, int(series_data[1]) + 1):
        url = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={series_data[0]}&Season={season_number}"
        tasks.append(session.get(url))
    return tasks


def get_episodes(session, episodes):
    tasks = []
    for episode in episodes:
        episode_imdb_id = episode["imdbID"]
        url = f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={episode_imdb_id}"
        tasks.append(session.get(url))
    return tasks


@shared_task
async def download_seasons(series_data):
    async with aiohttp.ClientSession() as session:
        seasons_tasks = get_seasons(session, series_data)
        response = await asyncio.gather(*seasons_tasks)
        seasons = []
        for season in response:
            seasons.append(await season.json())
        return seasons


@shared_task
async def download_episodes(episodes):
    async with aiohttp.ClientSession() as session:
        episodes_tasks = get_episodes(session, episodes)
        response = await asyncio.gather(*episodes_tasks)
        episodes = []
        for episode in response:
            episodes.append(await episode.json())
        return episodes