from django.db.models.fields import return_None
import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def signup_body():
    return {
        "email": "user@gmail.com",
        "password": "sTring32%21",
        "first_name": "телс",
        "last_name": "афдоафо",
        "patronymic": "фаощшфофо",
        "secret_word": "string"
    }


@pytest.fixture
def inactive_user(client, signup_url, signup_body):
    client.post(signup_url, data=signup_body)
    return User.objects.get(email=signup_body['email'])


@pytest.fixture
def active_user(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    confirm_code_id = response.data['confirm_code_id']
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    client.post(reverse('users:confirm_code', args=(code, confirm_code_id)))
    return User.objects.get(email=signup_body['email'])
