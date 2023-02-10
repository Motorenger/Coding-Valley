import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache

from discussions.models import Discussion, Comment


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Discussion)
def clear_discussions_cache(sender, instance, **kwargs):
    for key in cache.keys('*'):
        if 'discussions_viewset' in key.split('.'):
            cache.delete(key)
            logger.info(f'{sender.__name__}’s key: {key} was deleted')


@receiver(post_save, sender=Comment)
def clear_comments_cache(sender, instance, **kwargs):
    for key in cache.keys('*'):
        if 'comments_viewset' in key.split('.'):
            cache.delete(key)
            logger.info(f'{sender.__name__}’s key: {key} was deleted')
