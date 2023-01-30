import os
from datetime import datetime

import requests

from whatchlists.models import Movie


def get_omdb_by_search(search: str) -> dict:
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&s={search}").json()
    return data


def get_omdb_by_omdbid(omdb_id: str):
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    return data


def save_to_db_or_get(data: dict):
    '''Function takes data returned by imdb,
       distinguishes wheter it is movie of series,
       than saves it to the database if it is not saved yet
       returns instance
    '''

    # subfunction to save movie
    def save_movie(movie):
        # extracting only info needed for movie model
        needed_data = {}
        needed_data['title'] = movie['Title']

        # converting date format
        released = datetime.strptime(movie['Released'], '%d %b %Y').date()
        needed_data['released'] = released

        # editing runtime field
        needed_data['runtime'] = movie['Runtime'].split(' ')[0]

        needed_data['imdb_id'] = movie['imdbID']

        # initiation of the movie instance and saving
        movie = Movie(**needed_data)
        movie.save()

        return movie

    # subfunction to save series
    def save_series(series):
        pass

    # sorting by type (movie or series)
    data_type = data.get('Type', None)
    if data_type:
        if data_type == 'movie':

            # checking for existing movie
            try:
                movie = Movie.objects.get(imdb_id=data["imdbID"])
            except Movie.DoesNotExist:
                movie = save_movie(data)

            return movie

        elif data_type == 'series':
            pass

    return None
