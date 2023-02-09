from django.dispatch import receiver
from django.db.models.signals import post_save

from reviews.models import Review
from discussions.models import Discussion
from notifications.models import Notification


@receiver(post_save, sender=Review)
def review_created(sender, instance, created, **kwargs):
    if not created:
        return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type="review",
            review=instance,
            content=f"An review {instance.title} recently posted by {instance.user.userprofile.user}.",
        )


@receiver(post_save, sender=Discussion)
def discussion_created(sender, instance, created, **kwargs):
    if not created:
        return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type="discussion",
            discussion=instance,
            content=f"A discussion was started by {instance.user.userprofile.user}.",
        )
