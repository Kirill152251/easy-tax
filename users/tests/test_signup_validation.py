import pytest
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()


@pytest.mark.django_db
def test_invalid_password_whitespace_start(client, signup_url, signup_body):
    signup_body['password'] = ' 123fH678'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_password_whitespace_end(client, signup_url, signup_body):
    signup_body['password'] = '123fH678 '
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_first_name_double_dashes(client, signup_url, signup_body):
    signup_body['first_name'] = '--'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_first_name_contain_double_dashes(client, signup_url, signup_body):
    signup_body['first_name'] = 'афаа--афвф'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_first_name_contain_emoij(client, signup_url, signup_body):
    signup_body['first_name'] = '😁'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_secret_word_contain_emoij(client, signup_url, signup_body):
    signup_body['secret_word'] = '😁'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_invalid_secret_word_contain_digits(client, signup_url, signup_body):
    signup_body['secret_word'] = 'ывадфа9'
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

