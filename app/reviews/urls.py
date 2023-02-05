from django.urls import path, include
from rest_framework.routers import SimpleRouter

from reviews.viewsets import ReviewViewSet


router = SimpleRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')

app_name = "reviews_app"

urlpatterns = [
    path('', include(router.urls)),
]
