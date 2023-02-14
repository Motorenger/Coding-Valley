import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from watchlists.models import Media


class Discussion(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=400)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='discussions')
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='discussions', null=True, blank=True)

    class Meta:
        verbose_name = _('Discussion')
        verbose_name_plural = _('Discussions')
        ordering = ['-created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created']

    def __str__(self):
        return self.content[:50]
