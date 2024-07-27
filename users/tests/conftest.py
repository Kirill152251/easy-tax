
from django.utils.timezone import now
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from rest_framework.test import APIRequestFactory

from users.views import UserGetUpdateAPIView


User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def user_me_view():
    return UserGetUpdateAPIView.as_view()


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def user_me_url():
    return reverse('users:user_me')


@pytest.fixture
def signup_body():
    return {
        'email': 'user@gmail.com',
        'password': 'sTring32%21',
        'first_name': 'телс',
        'last_name': 'афдоафо',
        'patronymic': 'фаощшфофо',
        'secret_word': 'слово'
    }


@pytest.fixture
def full_update_body():
    return {
        'email': 'user12@gmail.com',
        'first_name': 'новоеимя',
        'last_name': 'новаяфамилия',
        'patronymic': 'отчество',
        'unp': '1751981489',
        'registration_address': 'аофдлаофда',
        'residential_address': 'оазфзоф',
        'date_of_birth': now().date()
    }


@pytest.fixture
def partial_update_body():
    return {
        'email': 'user12@gmail.com',
        'last_name': 'новаяфамилия',
        'patronymic': 'отчество',
        'registration_address': 'аофдлаофда',
        'date_of_birth': now().date()
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
