from django.urls import path

from watchlists import views


app_name = 'watchlists_app'

urlpatterns = [
    path('search/', views.search_by_search_view, name='search'),
    path('recently_searched/', views.RecentlySearched.as_view(), name='recently_searched'),
    path('get/', views.GetByOmdbIdView.as_view(),  name='get_by_omdbid'),
    path('get/season/', views.GetSeason.as_view(), name='get_season_by_omdbid')
]
