import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
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


@pytest.mark.django_db
def test_same_email_but_uppercase(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_201_CREATED
    confirm_code_id = response.data['confirm_code_id']
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    response = client.post(reverse('users:confirm_code', args=(code, confirm_code_id)))
    assert response.status_code == status.HTTP_200_OK
    new_body = {
        'email': 'USER@gmail.com',
        'password': 'sTring32%21',
        'first_name': 'телс',
        'last_name': 'афдоафо',
        'patronymic': 'фаощшфофо',
        'secret_word': 'слово'
    }
    response = client.post(signup_url, data=new_body)
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_signup_without_email(client, signup_url, signup_body):
    signup_body.pop('email')
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
