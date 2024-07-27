import pytest
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param,value',
    [
        ('first_name', 'плаыдфаф '),
        ('last_name', ' плаыдфаф'),
        ('patronymic', 'плаы дфаф'),
        ('password', ' 123 Kdf032 '),
        ('secret_word', ' плаы дфаф '),
    ]
)
def test_invalid_params_contain_space(client, signup_url, signup_body, param, value):
    signup_body[param] = value
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param,value',
    [
        ('first_name', 'плаыдфафдддддддддддддддддддддддддддддддддддддддддддддддд'),
        ('last_name', 'плаыдфафффффффффффффффффффффффффффффффффффффффффффффф'),
        ('patronymic', 'плаыдфафффффффффффффффффффффффффффффффффффффффффффффффффф'),
    ]
)
def test_fio_max_len(client, signup_url, signup_body, param, value):
    signup_body[param] = value
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param',
    ('first_name', 'last_name', 'patronymic')
)
def test_invalid_fio_contaion_double_dashes(client, signup_url, signup_body, param):
    signup_body[param] = 'афаа--афвф'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param',
    ('first_name', 'last_name', 'patronymic', 'secret_word', 'password')
)
def test_invalid_params_contain_emoij(client, signup_url, signup_body, param):
    signup_body[param] = '😁'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_secret_word_contain_digits(client, signup_url, signup_body):
    signup_body['secret_word'] = 'ывадфа9'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'fio',
    ('first_name', 'last_name', 'patronymic')
)
def test_fio_only_dashe(client, signup_url, signup_body, fio):
    signup_body[fio] = '-'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
