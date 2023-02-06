from django.db import models

from whatchlists import models as m


class MovieManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs) \
            .filter(media_type=m.Media.MediaTypes.MOVIE)


class SeriesManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs) \
            .filter(media_type=m.Media.MediaTypes.SERIES)
