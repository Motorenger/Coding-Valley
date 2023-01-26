from django.db import models
from django.utils.translation import gettext as _


import uuid


class Movie(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    released = models.DateField(_("Release date"))
    runtime = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.name
