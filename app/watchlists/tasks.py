import asyncio
import os

import aiohttp
from celery import shared_task


def get_seasons(session, series_data):
    tasks = []
    for season_number in range(1, int(series_data[1]) + 1):
        url = f'https://www.omdbapi.com?apikey={os.environ.get("API_KEY")}&i={series_data[0]}&Season={season_number}'
        tasks.append(session.get(url))
    return tasks


def get_episodes(session, episodes):
    tasks = []
    for episode in episodes:
        episode_imdb_id = episode['imdbID']
        url = f'https://www.omdbapi.com?apikey={os.environ.get("API_KEY")}&i={episode_imdb_id}'
        tasks.append(session.get(url))
    return tasks


async def download_seasons(series_data):
    async with aiohttp.ClientSession() as session:
        seasons_tasks = get_seasons(session, series_data)
        response = await asyncio.gather(*seasons_tasks)
        seasons = [await season.json() for season in response]
        return seasons


async def download_episodes(episodes):
    async with aiohttp.ClientSession() as session:
        episodes_tasks = get_episodes(session, episodes)
        response = await asyncio.gather(*episodes_tasks)
        episodes = []
        episodes = [await episode.json() for episode in response]
        return episodes


@shared_task
def get_season_data(series_data):
    return asyncio.run(download_seasons(series_data))


@shared_task
def get_episode_data(episodes):
    return asyncio.run(download_episodes(episodes))
