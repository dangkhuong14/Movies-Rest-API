from django.urls import path
from watchlist_app.views import movie_list
from watchlist_app.views import movie_details

urlpatterns = [
    path('list/', movie_list, name='movie-list'),
    path('<int:pk>/', movie_details, name='movie-details')
]
