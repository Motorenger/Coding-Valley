import logging
import datetime

import requests

from watchlists.services import omdb_requests as req
from watchlists.models import Movie, Series
from watchlists.tasks import download_episodes


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
    session = requests.Session()
    series_data = req.get_omdb_by_omdbid(imdb_id, session)
    released = datetime.datetime.strptime(series_data['Released'], '%d %b %Y').date()

    needed_data = {}
    needed_data['title'] = series_data['Title']
    needed_data['year'] = series_data['Year']
    needed_data['released'] = released
    needed_data['genres'] = series_data['Genre']
    needed_data['plot'] = series_data['Plot']
    needed_data['total_seasons'] = series_data['totalSeasons']
    needed_data['runtime'] = series_data['Runtime'].split(' ')[0]
    needed_data['poster'] = series_data['Poster']
    needed_data['imdb_id'] = series_data['imdbID']
    needed_data['imdb_rating'] = series_data['imdbRating']
    runtime = series_data['Runtime'].split(' ')[0]

    if runtime not in ["N/A"]:
        needed_data['runtime'] = runtime

    series = Series(**needed_data)
    series.save()

    try:
        download_episodes.delay(series).get()
    except Exception as e:
        logger.error(f'detail: {e}')

    return series
