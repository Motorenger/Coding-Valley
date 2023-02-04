import uuid

from django.db import models
from django.utils.translation import gettext as _


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    released = models.DateField(_("Release date"))
    runtime = models.PositiveIntegerField()
    genres = models.CharField(max_length=255)
    poster = models.URLField(max_length=200)
    imdb_id = models.CharField(max_length=50)
    imdb_rating = models.FloatField()

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title

    def get_runtime(self):
        return f"{self.runtime}m"

    def get_year(self):
        return self.released.year


class Series(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    year = models.CharField(max_length=9, help_text="Use such format: 2018-2022")
    released = models.DateField(_("Release date"))
    genres = models.CharField(max_length=255)
    plot = models.TextField()
    total_seasons = models.PositiveIntegerField()
    poster = models.URLField(max_length=200)
    imdb_id = models.CharField(max_length=50)
    imdb_rating = models.FloatField()

    class Meta:
        verbose_name = _("Series")
        verbose_name_plural = _("Series")

    def __str__(self):
        return self.title


class Season(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    season_numb = models.PositiveIntegerField()
    total_episodes = models.PositiveIntegerField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="seasons")

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
        ordering = ["season_numb"]

    def __str__(self):
        return f"{self.series} s. {self.season_numb}"


class Episode(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    released = models.DateField()
    episode_numb = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    plot = models.TextField()
    poster = models.URLField(max_length=200)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    imdb_rating = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")
        ordering = ["episode_numb"]

    def __str__(self):
        return self.title
