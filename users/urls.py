from django.urls import path

from users.views import SignupAPIView, confirm_code


urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('confirm_code/<int:code>/<str:code_id>/', confirm_code, name='confirm_code'),
]

