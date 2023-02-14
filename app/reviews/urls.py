from django.urls import path, include
from rest_framework.routers import SimpleRouter

from reviews.viewsets import ReviewViewSet, ReviewLikeViewSet


router = SimpleRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'reviewlikes', ReviewLikeViewSet, basename='reviewlikes')

app_name = 'reviews_app'

urlpatterns = [
    path('', include(router.urls)),
]
