import re

from django.core.paginator import Paginator
from rest_framework import serializers

from reviews.serializers import ReviewSerializer
from watchlists.models import (Media, Movie, Series, Season, Episode)


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'released', 'genres', 'poster', 'plot', 'imdb_id', 'imdb_rating', 'media_type']


class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField('get_paginated_reviews')

    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'released', 'genres', 'poster', 'imdb_rating', 'reviews']

    def get_paginated_reviews(self, obj):
        page_size = self.context['request'].query_params.get('size', 5)
        page_number = self.context['request'].query_params.get('page', 1)
        full_path = self.context['request'].get_full_path()
        url_without_page_query_param = re.sub(r"&page=\d+", "", full_path)
        url_without_page_and_size_query_params = re.sub(r"&size=\d*", "", url_without_page_query_param)
        paginator = Paginator(obj.reviews.all(), page_size)
        page = self.get_page(paginator, page_size, page_number, url_without_page_and_size_query_params)
        return page

    def get_page(self, paginator, page_size, page_number, url):
        context = {'request': self.context['request']}
        page_obj = paginator.page(page_number)
        page = {
            "count": paginator.count,
            "next": self.get_next_link(url, page_size, page_obj),
            "previous": self.get_previous_link(url, page_size, page_obj),
            "results": ReviewSerializer(page_obj, many=True, context=context).data
        }
        return page

    @staticmethod
    def get_next_link(url, page_size, page_obj):
        if page_obj.has_next():
            return f"{url}&size={page_size}&page={page_obj.next_page_number()}"
        return None

    @staticmethod
    def get_previous_link(url, page_size, page_obj):
        if page_obj.has_previous():
            return f"{url}&size={page_size}&page={page_obj.previous_page_number()}"
        return None


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'released', 'episode_numb', 'runtime', 'plot', 'poster', 'imdb_rating']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = ['season_numb', 'total_episodes', 'episodes']

    def get_episodes(self, instance):
        imdb_rating = self.context["imdb_rating"]
        if imdb_rating is not None:
            episodes = instance.episodes.filter(imdb_rating__gte=imdb_rating)
        else:
            episodes = instance.episodes.all()
        return EpisodeSerializer(episodes, many=True).data


class SeriesSerializer(MovieSerializer):
    # seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'year', 'released', 'genres', 'plot', 'imdb_rating', 'total_seasons', "poster", "reviews", "seasons"]
        depth = 2
