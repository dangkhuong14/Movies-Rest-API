from django.urls import path
from watchlist_app.api.views import MovieListAV
from watchlist_app.api.views import MovieDetailAV

urlpatterns = [
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailAV.as_view(), name='movie-detail')
]
