from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListAV, WatchDetailAV,
                                     StreamPlatformAV, StreamPlatformDetailAV,
                                     ReviewList, ReviewCreate, ReviewDetail,
                                     StreamPlatformVS)

router = DefaultRouter()
router.register(r'streams', StreamPlatformVS, basename='stream-platform')

urlpatterns = [
    # watchlist
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watch-detail'),

    # streaming platform
    #     path('stream/', StreamPlatformAV.as_view(),
    #          name='stream-list'),
    #     path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(),
    #          name='stream-detail'),
    path('', include(router.urls)),

    # review
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-detail'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail')
]
