import os
from datetime import datetime

import requests

from whatchlists.models import Movie, Series, Season, Episode


def get_omdb_by_search(search: str) -> dict:
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&s={search}").json()
    return data


def get_omdb_by_omdbid(omdb_id: str):
    data = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={omdb_id}").json()
    return data


def get_season_by_omdbid(series_omdb_id: str, season_numb: int) -> dict:
    season = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={series_omdb_id}&Season={season_numb}").json()
    return season


def get_episode_by_omdbid(episode_omdb_id: str) -> dict:
    episode = requests.get(f"https://www.omdbapi.com?apikey={os.environ.get('API_KEY')}&i={episode_omdb_id}").json()
    return episode


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
    def save_series(series_data):
        """At first saves series then iterated through
           season and series which also saves,
           returns series instance
        """

        # extracting only info needed for series model
        needed_data = {}
        needed_data['title'] = series_data['Title']
        needed_data['year'] = series_data['Year']

        # converting date format
        released = datetime.strptime(series_data['Released'], '%d %b %Y').date()
        needed_data['released'] = released

        needed_data['plot'] = series_data['Plot']
        needed_data['total_seasons'] = series_data['totalSeasons']
        needed_data['imdb_id'] = series_data['imdbID']

        # initiation of the movie instance and saving
        series = Series(**needed_data)
        series.save()

        # iterationg through seasons
        for season_number in range(1, int(series.total_seasons)+1):
            season_data = get_season_by_omdbid(series.imdb_id, season_number)

            # extracting only info needed for season model
            needed_data = {}
            needed_data['season_numb'] = season_data['Season']
            needed_data['total_episodes'] = 0

            season = Season(series=series, **needed_data)

            # iterating through episodes
            episodes = []
            for e in season_data["Episodes"]:
                episode_data = get_episode_by_omdbid(e["imdbID"])
                if not episode_data["Response"]:
                    break
                # extracting only info needed for series model
                needed_data = {}
                needed_data['title'] = episode_data['Title']

                # converting date format
                released = datetime.strptime(series_data['Released'], '%d %b %Y').date()
                needed_data['released'] = released

                needed_data['episode_numb'] = episode_data['Episode']
                # editing runtime field
                needed_data['runtime'] = episode_data['Runtime'].split(" ")[0]
                needed_data['plot'] = episode_data['Plot']

                episode = Episode(season=season, **needed_data)
                episodes.append(episode)

            season.total_episodes += len(episodes)
            season.save()
            Episode.objects.bulk_create(episodes)
        return series

    # sorting by type (movie or series)
    data_type = data.get('Type', None)
    if data_type:
        if data_type == 'movie':

            # checking for existing movie
            try:
                movie = Movie.objects.get(imdb_id=data["imdbID"])
            except Movie.DoesNotExist:
                movie = save_movie(data), "movie"

            return movie

        elif data_type == 'series':
            try:
                series = Series.objects.get(imdb_id=data["imdbID"])
            except Series.DoesNotExist:
                series = save_series(data)
            return series, "series"
    return None
