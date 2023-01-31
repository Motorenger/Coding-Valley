import uuid

from django.db import models
from django.utils.translation import gettext as _


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.title


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    released = models.DateField(_("Release date"))
    runtime = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    imdb_id = models.CharField(max_length=50)

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
    genres = models.ManyToManyField(Genre, related_name="series")
    plot = models.TextField()
    total_seasons = models.PositiveIntegerField()
    imdb_id = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Series")
        verbose_name_plural = _("Series")

    def __str__(self):
        return self.title


class Season(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    season_numb = models.PositiveIntegerField()
    total_episodes = models.PositiveIntegerField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")

    def __str__(self):
        return f"{self.series} s. {self.season}"


class Episode(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    released = models.DateField()
    episode_numb = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    plot = models.TextField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")

    def __str__(self):
        return self.title
