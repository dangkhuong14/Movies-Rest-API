from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from user_app.api.views import registration_view, logout_view, jwt_registration_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Token Authentication URLs:
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),


    # JWT Authentication URLs:
    path('register-jwt/', jwt_registration_view, name='register-jwt'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
