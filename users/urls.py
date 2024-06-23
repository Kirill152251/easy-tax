from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from users.views import SignupAPIView, confirm_code


app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('confirm_code/<int:code>/<str:confirm_code_id>/', confirm_code, name='confirm_code'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
