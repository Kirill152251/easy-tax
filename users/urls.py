from django.urls import include, path

from users.views import RegistrationView, confirm_code


urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('confirm_code/<int:code>/<int:code_id>/', confirm_code, name='confirm_code'),
]

