import uuid

from django.db import models
from django.utils.translation import gettext as _

from users.models import User
from movies.models import Movie


class Discussion(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussions")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="discussions", null=True, blank=True)

    class Meta:
        verbose_name = _("Discussion")
        verbose_name_plural = _("Discussions")

    def __str__(self):
        return self.title
