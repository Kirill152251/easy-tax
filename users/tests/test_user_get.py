import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate


User = get_user_model()


def test_anonymous_user_cant_get_user_me(
    factory,
    get_user_url,
    get_view
):
    request = factory.get(get_user_url)
    response = get_view(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inactive_user_cant_get_user_me(
    factory,
    get_user_url,
    get_view,
    inactive_user
):
    request = factory.get(get_user_url)
    force_authenticate(request, user=inactive_user)
    response = get_view(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_me_success(
    factory,
    get_user_url,
    get_view,
    active_user
):
    request = factory.get(get_user_url)
    force_authenticate(request, user=active_user)
    response = get_view(request)
    assert response.status_code == status.HTTP_200_OK
    assert str(active_user.id) == response.data['id']
