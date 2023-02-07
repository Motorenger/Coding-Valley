from django.urls import path, include

from watchlists import views


urlpatterns = [
    path("search/", views.search_by_search_view),
    path("get/", views.GetByOmdbIdView.as_view()),
    path("get/season/", views.GetSeason.as_view())
]
