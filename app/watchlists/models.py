import uuid

from django.db import models
from django.utils.translation import gettext as _

from watchlists.managers import MovieManager, SeriesManager


class Media(models.Model):

    class MediaTypes(models.TextChoices):
        MOVIE = "MOVIE", "Movie"
        SERIES = "SERIES", "Series"

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    released = models.DateField(_("Release date"))
    genres = models.CharField(max_length=255)
    poster = models.URLField(max_length=200)
    plot = models.TextField()
    imdb_id = models.CharField(max_length=50)
    imdb_rating = models.FloatField()
    media_type = models.CharField(max_length=6, choices=MediaTypes.choices)

    # only movie
    runtime = models.PositiveIntegerField(null=True, blank=True)

    # only series
    total_seasons = models.PositiveIntegerField(null=True, blank=True)
    year = models.CharField(max_length=9, help_text="Use such format: 2018-2022", null=True, blank=True)

    def __str__(self):
        return self.title


class Movie(Media):
    objects = MovieManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.media_type = Media.MediaTypes.MOVIE
        return super().save(*args, **kwargs)


class Series(Media):
    objects = SeriesManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.media_type = Media.MediaTypes.SERIES
        return super().save(*args, **kwargs)


class Season(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    season_numb = models.PositiveIntegerField()
    total_episodes = models.PositiveIntegerField()
    series = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="seasons")

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
