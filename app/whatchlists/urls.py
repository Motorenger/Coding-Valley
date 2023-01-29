from django.urls import path, include
from rest_framework import routers

from whatchlists import views


router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("search/", views.search_by_search_test_view),
    path("get/", views.search_by_omdbid_test_view)
]
