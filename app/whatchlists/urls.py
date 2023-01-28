from django.urls import path, include
from rest_framework import routers

from whatchlists import views


router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)


urlpatterns = [
    path("", include(router.urls))
]
