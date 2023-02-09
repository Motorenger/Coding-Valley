import datetime

import requests


from . import omdb_requests as req
from watchlists.models import Movie, Series, Season, Episode


def save_movie(imdb_id):
    """Creates movie and returns it"""

    movie_data = req.get_omdb_by_omdbid(imdb_id)

    # extracting only info needed for movie model
    needed_data = {}
    needed_data['title'] = movie_data['Title']

    # converting date format
    released = datetime.datetime.strptime(movie_data['Released'], '%d %b %Y').date()
    needed_data['released'] = released

    # editing runtime field
    needed_data['runtime'] = movie_data['Runtime'].split(' ')[0]

    needed_data['genres'] = movie_data['Genre']
    needed_data['poster'] = movie_data['Poster']
    needed_data['imdb_id'] = movie_data['imdbID']
    needed_data['imdb_rating'] = movie_data['imdbRating']
    needed_data['last_retrieved'] = datetime.datetime.today().date() - datetime.timedelta(days=1)

    # initiation of the movie instance and saving
    movie = Movie(**needed_data)
    movie.save()

    return movie


def save_series(imdb_id):
    """At first saves series then iterated through
        season and episodes and saves them too,
        returns series instance
    """
    session = requests.Session()

    series_data = req.get_omdb_by_omdbid(imdb_id, session)

    # extracting only info needed for series model
    needed_data = {}
    needed_data['title'] = series_data['Title']
    needed_data['year'] = series_data['Year']

    # converting date format
    released = datetime.strptime(series_data['Released'], '%d %b %Y').date()
    needed_data['released'] = released

    needed_data['genres'] = series_data['Genre']
    needed_data['plot'] = series_data['Plot']
    needed_data['total_seasons'] = series_data['totalSeasons']
    needed_data['poster'] = series_data['Poster']
    needed_data['imdb_id'] = series_data['imdbID']
    needed_data['imdb_rating'] = series_data['imdbRating']

    # initiation of the movie instance and saving
    series = Series(**needed_data)
    series.save()

    # iterationg through seasons
    for season_number in range(1, int(series.total_seasons)+1):
        season_data = req.get_season_by_omdbid(series.imdb_id, season_number, session)

        # extracting only info needed for season model
        needed_data = {}
        needed_data['season_numb'] = season_data['Season']
        needed_data['total_episodes'] = 0

        season = Season(series=series, **needed_data)

        # iterating through episodes
        episodes = []
        for e in season_data["Episodes"]:
            episode_data = req.get_episode_by_omdbid(e["imdbID"], session)
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
            needed_data['poster'] = episode_data['Poster']
            imdb_rating = episode_data['imdbRating']

            if imdb_rating not in ["N/A"]:
                needed_data['imdb_rating'] = imdb_rating

            episode = Episode(season=season, **needed_data)
            episodes.append(episode)

        season.total_episodes += len(episodes)
        season.save()
        Episode.objects.bulk_create(episodes)
    return series
