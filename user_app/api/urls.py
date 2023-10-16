from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from user_app.api.views import registration_view, logout_view

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout')
]
