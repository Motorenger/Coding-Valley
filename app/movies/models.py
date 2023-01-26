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

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title

    def get_runtime(self):
        return f"{self.runtime}m"

    def get_year(self):
        return self.released.year
