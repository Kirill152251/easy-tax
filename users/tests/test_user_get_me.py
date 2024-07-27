import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate


User = get_user_model()


def test_anonymous_user_cant_get_user_me(
    factory,
    user_me_url,
    user_me_view
):
    request = factory.get(user_me_url)
    response = user_me_view(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inactive_user_cant_get_user_me(
    factory,
    user_me_url,
    user_me_view,
    inactive_user
):
    request = factory.get(user_me_url)
    force_authenticate(request, user=inactive_user)
    response = user_me_view(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_me_success(
    factory,
    user_me_url,
    user_me_view,
    active_user
):
    request = factory.get(user_me_url)
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status.HTTP_200_OK
    assert str(active_user.id) == response.data['id']
