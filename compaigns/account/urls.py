from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from .views import UserRegister

urlpatterns = [
    # jwt_endpoint
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # my_endpoints
    path('register/', UserRegister.as_view(), name='register_user')
]
