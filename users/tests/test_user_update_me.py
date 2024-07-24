import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate


User = get_user_model()


def test_anonymous_user_cant_update_user_me(
    factory,
    user_me_url,
    user_me_view,
):
    request = factory.patch(user_me_url, {'first_name': 'новоеимя'})
    response = user_me_view(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inactive_user_cant_update_user_me(
    factory,
    user_me_url,
    user_me_view,
    inactive_user
):
    request = factory.patch(user_me_url, {'first_name': 'новоеимя'})
    force_authenticate(request, user=inactive_user)
    response = user_me_view(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_partial_update_me_success(
    factory,
    user_me_url,
    user_me_view,
    active_user,
    partial_update_body
):
    request = factory.patch(user_me_url, partial_update_body)
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    user = User.objects.all().first()
    assert response.status_code == status.HTTP_200_OK
    assert user.email == partial_update_body['email'] 
    assert user.last_name == partial_update_body['last_name'] 
    assert user.patronymic == partial_update_body['patronymic'] 
    assert user.registration_address == partial_update_body['registration_address'] 
    assert user.date_of_birth == partial_update_body['date_of_birth'] 


@pytest.mark.django_db
def test_full_update_me_success(
    factory,
    user_me_url,
    user_me_view,
    active_user,
    full_update_body
):
    request = factory.patch(user_me_url, full_update_body)
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    user = User.objects.all().first()
    assert response.status_code == status.HTTP_200_OK
    assert user.email == full_update_body['email'] 
    assert user.first_name == full_update_body['first_name'] 
    assert user.last_name == full_update_body['last_name'] 
    assert user.patronymic == full_update_body['patronymic'] 
    assert user.unp == full_update_body['unp']
    assert user.registration_address == full_update_body['registration_address'] 
    assert user.residential_address == full_update_body['residential_address'] 
    assert user.date_of_birth == full_update_body['date_of_birth'] 
