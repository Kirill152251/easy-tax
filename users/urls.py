from django.urls import path

from users.views import SignupAPIView, confirm_code


app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('confirm_code/<int:code>/<str:confirm_code_id>/', confirm_code, name='confirm_code'),
]

