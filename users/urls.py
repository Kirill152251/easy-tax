from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from users.views import (
    SignupAPIView,
    confirm_code,
    get_orders_sum,
    UserAvatarAPIView,
    UserGetUpdateAPIView,
    UserProductsListAPIView,
    UserOrdersListAPIView,
    UserOrdersToBuyListAPIView
)


app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('confirm_code/<int:code>/<str:confirm_code_id>/', confirm_code, name='confirm_code'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', UserGetUpdateAPIView.as_view(), name='user_me'),
    path('users/me/avatar/', UserAvatarAPIView.as_view(), name='user_avatar'),
    path('users/me/products/', UserProductsListAPIView.as_view(), name='user_products'),
    path('users/me/orders/', UserOrdersListAPIView.as_view(), name='user_orders'),
    path('users/me/orders_to_buy/', UserOrdersToBuyListAPIView.as_view(), name='user_orders_to_buy'),
    path('users/me/orders/sum/', get_orders_sum, name='orders_sum'),
]
