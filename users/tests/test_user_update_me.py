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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param,value',
    [
        ('first_name', ' фдадфаол'),
        ('last_name', ' плаыдфаф '),
        ('patronymic', ' плаыдфаф '),
        ('first_name', 'фдадфаолллллллллллллллллллллллл'),
        ('last_name', 'плаыдфафвввввввввввввввввввввввв'),
        ('patronymic', 'плаыдфафйййййййййййййййййййййййо'),
    ]
)
def test_invalid_fio(
    factory,
    user_me_url,
    user_me_view,
    active_user,
    full_update_body,
    param,
    value
):
    full_update_body[param] = value
    request = factory.patch(user_me_url, full_update_body)
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'date,status',
    [
        ('2224-08-13', status.HTTP_400_BAD_REQUEST),
        ('1904-08-11', status.HTTP_400_BAD_REQUEST),
        ('2001-06-22', status.HTTP_200_OK),
    ]
)
def test_date_of_birth_patch(
    factory,
    user_me_url,
    active_user,
    user_me_view,
    date,
    status
):
    request = factory.patch(user_me_url, {'date_of_birth': date})
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'value,status',
    [
        ('FAL349A4L', status.HTTP_200_OK),
        ('999225345', status.HTTP_200_OK),
        ('PFAMUKRFQ', status.HTTP_400_BAD_REQUEST),
        ('', status.HTTP_400_BAD_REQUEST),
        ('FALJ30ALJF92A', status.HTTP_400_BAD_REQUEST),
        ('FALK20VA', status.HTTP_400_BAD_REQUEST),
        ('afa932faa', status.HTTP_400_BAD_REQUEST),
    ]
)
def test_unp_patch(
    factory,
    user_me_url,
    active_user,
    user_me_view,
    value,
    status
):
    request = factory.patch(user_me_url, {'unp': value})
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'value,status',
    [
        ('MP2931048', status.HTTP_200_OK),
        ('', status.HTTP_400_BAD_REQUEST),
        ('M29401840', status.HTTP_400_BAD_REQUEST),
        ('MP2913', status.HTTP_400_BAD_REQUEST),
        ('310092999', status.HTTP_400_BAD_REQUEST),
        ('MP981841981', status.HTTP_400_BAD_REQUEST),
        ('MP8329K23', status.HTTP_400_BAD_REQUEST),
    ]
)
def test_passport_num_patch(
    factory,
    user_me_url,
    active_user,
    user_me_view,
    value,
    status
):
    request = factory.patch(user_me_url, {'passport_num': value})
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'value,status',
    [
        ('+375447777777', status.HTTP_200_OK),
        ('', status.HTTP_400_BAD_REQUEST),
        ('      ', status.HTTP_400_BAD_REQUEST),
        ('375449999999', status.HTTP_400_BAD_REQUEST),
        ('+3753291', status.HTTP_400_BAD_REQUEST),
        ('+375j91092222', status.HTTP_400_BAD_REQUEST),
        ('+37593919199310', status.HTTP_400_BAD_REQUEST),
    ]
)
def test_phone_num_patch(
    factory,
    user_me_url,
    active_user,
    user_me_view,
    value,
    status
):
    request = factory.patch(user_me_url, {'phone_number': value})
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'value,status',
    [
        ('ул. Колотушкина, д.2222, кв. 21', status.HTTP_200_OK),
        ('', status.HTTP_400_BAD_REQUEST),
        ('        ', status.HTTP_400_BAD_REQUEST),
        ('ул. Kalfjanfal, д.2222, кв. 21', status.HTTP_400_BAD_REQUEST),
    ]
)
def test_addresses_patch(
    factory,
    user_me_url,
    active_user,
    user_me_view,
    value,
    status
):
    request = factory.patch(
        user_me_url,
        {'residential_address': value, 'registration_address': value}
    )
    force_authenticate(request, user=active_user)
    response = user_me_view(request)
    assert response.status_code == status
