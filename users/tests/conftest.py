import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from rest_framework.test import APIRequestFactory

from users.views import GetUserAPIView


User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def get_view():
    return GetUserAPIView.as_view()


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def get_user_url():
    return reverse('users:get_user')


@pytest.fixture
def signup_body():
    return {
        "email": "user@gmail.com",
        "password": "sTring32%21",
        "first_name": "телс",
        "last_name": "афдоафо",
        "patronymic": "фаощшфофо",
        "secret_word": "слово"
    }

@pytest.fixture
def active_user(signup_body):
    user = User(**signup_body)
    user.is_active = True
    user.save()
    return user 


@pytest.fixture
def inactive_user(signup_body):
    user = User(**signup_body)
    user.save()
    return user 
