import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

from whatchlists.models import Media


class Review(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=150)
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews", editable=False)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="reviews")
    created = models.DateField(auto_now_add=True)
    stars = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    likes = models.ManyToManyField(get_user_model(), through="ReviewLikes", through_fields=('review', 'user'))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.title


class ReviewLikes(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="users_liked")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews_liked")
    like = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("ReviewLikes")
        verbose_name_plural = _("ReviewLikes")
