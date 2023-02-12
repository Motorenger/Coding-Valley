import random

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def series_tt1234567():
    """Create series with tt1234567 id in db."""
    series = baker.prepare("watchlists.Series")
    for season_numb in range(3):
        episodes_list = [baker.make("watchlists.Episode", imdb_rating=random.uniform(1, 10)) for _ in range(10)]
        season = baker.prepare("watchlists.Season")
        season.episodes.add(*episodes_list)
        season.season_numb = season_numb
        season.save()
        series.seasons.add(season)
    series.imdb_id = "tt1234567"
    series.save()
    return series
