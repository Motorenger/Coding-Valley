from django.urls import path, include
from rest_framework import routers

from whatchlists import views


router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
# router.register(r'series', views.SeriesViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("search/", views.search_by_search_view),
    path("get/", views.GetByOmdbIdView.as_view()),
    # path("get/season/", views.GetSeason.as_view())
]
