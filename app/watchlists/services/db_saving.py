import logging
import datetime
import asyncio

import requests


from watchlists.services import omdb_requests as req
from watchlists.models import Movie, Series, Season, Episode
from watchlists.tasks import get_season_data, get_episode_data


logger = logging.getLogger(__name__)


def save_movie(imdb_id):
    """
        Creates movie and returns it
    """

    movie_data = req.get_omdb_by_omdbid(imdb_id)
    released = datetime.datetime.strptime(movie_data['Released'], '%d %b %Y').date()

    needed_data = {}
    needed_data['title'] = movie_data['Title']
    needed_data['released'] = released
    needed_data['runtime'] = movie_data['Runtime'].split(' ')[0]
    needed_data['genres'] = movie_data['Genre']
    needed_data['poster'] = movie_data['Poster']
    needed_data['imdb_id'] = movie_data['imdbID']
    needed_data['imdb_rating'] = movie_data['imdbRating']
    needed_data['last_retrieved'] = datetime.datetime.today().date() - datetime.timedelta(days=1)

    movie = Movie(**needed_data)
    movie.save()

    return movie


def save_series(imdb_id):
    """
        At first saves series then iterated through
        season and episodes and saves them too,
        returns series instance
    """

    # getting series data from imdb_api
    series_data = req.get_omdb_by_omdbid(imdb_id)
    released = datetime.datetime.strptime(series_data['Released'], '%d %b %Y').date()

    # extracting data for series
    needed_data = {}
    needed_data['title'] = series_data['Title']
    needed_data['year'] = series_data['Year']
    needed_data['released'] = released
    needed_data['genres'] = series_data['Genre']
    needed_data['plot'] = series_data['Plot']
    needed_data['total_seasons'] = series_data['totalSeasons']
    needed_data['poster'] = series_data['Poster']
    needed_data['imdb_id'] = series_data['imdbID']
    needed_data['imdb_rating'] = series_data['imdbRating']

    series = Series(**needed_data)
    series.save()

    # prepare data for seasons
    series_data = (series.imdb_id, series.total_seasons)
    seasons = get_season_data.delay(series_data).get()
    seasons_all = []

    for season_data in seasons:

        # extracting data for season
        needed_data = {}
        needed_data['season_numb'] = season_data['Season']
        needed_data['total_episodes'] = 0

        season = Season(**needed_data)
        season.save()
        seasons_all.append(season)

        # prepare data for episodes
        episodes = season_data["Episodes"]
        episodes = get_episode_data.delay(episodes).get()
        episodes_all = []

        for episode_data in episodes:

            # extracting data for episode
            needed_data = {}
            needed_data['title'] = episode_data['Title']
            needed_data['released'] = datetime.datetime.strptime(episode_data['Released'], '%d %b %Y').date()
            needed_data['episode_numb'] = episode_data['Episode']
            needed_data['plot'] = episode_data['Plot']
            needed_data['poster'] = episode_data['Poster']

            imdb_rating = episode_data['imdbRating']
            if imdb_rating not in ["N/A"]:
                needed_data['imdb_rating'] = imdb_rating

            runtime = episode_data['Runtime'].split(" ")[0]
            if runtime not in ["N/A"]:
                needed_data['runtime'] = runtime

            episode = Episode(**needed_data)
            episodes_all.append(episode)

        Episode.objects.bulk_create(episodes_all)
        season.total_episodes += len(episodes_all)
        season.episodes.add(*episodes_all)

    [season.save() for season in seasons_all]
    series.seasons.add(*seasons_all)
    series.save()

    return series
