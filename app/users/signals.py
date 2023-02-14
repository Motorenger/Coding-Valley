import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import User, UserProfile


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f'Profile {instance} was created.')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    logger.info(f'Profile {instance} was saved.')
