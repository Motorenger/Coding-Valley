import datetime

import requests

from celery import shared_task

from watchlists.services import omdb_requests as req
from watchlists.models import Series, Season, Episode


@shared_task
def download_episodes(series_id):
    session = requests.Session()
    series = Series.objects.get(id=series_id)
    for season_number in range(1, int(series.total_seasons) + 1):
        season_data = req.get_season_by_omdbid(series.imdb_id, season_number, session)
        needed_data = {}
        needed_data['season_numb'] = season_data['Season']
        needed_data['total_episodes'] = 0
        season = Season(series=series, **needed_data)

        episodes = []
        for episode in season_data["Episodes"]:
            episode_data = req.get_episode_by_omdbid(episode["imdbID"], session)
            if not episode_data["Response"]:
                break

            needed_data = {}
            needed_data['title'] = episode_data['Title']
            needed_data['released'] = datetime.datetime.strptime(episode_data['Released'], '%d %b %Y').date()
            needed_data['episode_numb'] = episode_data['Episode']
            needed_data['runtime'] = episode_data['Runtime'].split(" ")[0]
            needed_data['plot'] = episode_data['Plot']
            needed_data['poster'] = episode_data['Poster']
            imdb_rating = episode_data['imdbRating']
            if imdb_rating not in ["N/A"]:
                needed_data['imdb_rating'] = imdb_rating

            episode = Episode(season=season, **needed_data)
            episodes.append(episode)
        season.total_episodes += len(episodes)
        season.save()
        Episode.objects.bulk_create(episodes)
    return f'Series: {series.title}'
