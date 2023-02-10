import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache

from reviews.models import Review


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Review)
def clear_reviews_cache(sender, instance, **kwargs):
    for key in cache.keys('*'):
        if 'reviews_viewset' in key.split('.'):
            cache.delete(key)
            logger.info(f'{sender.__name__}’s key: {key} was deleted')


@receiver(post_save, sender=Review)
def clear_review_cache(sender, instance, **kwargs):
    for key in cache.keys('*'):
        if 'review_viewset' in key.split('.'):
            cache.delete(key)
            logger.info(f'{sender.__name__}’s key: {key} was deleted')
