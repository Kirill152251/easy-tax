import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone
from rest_framework import status

from users.models import SignupSession


User = get_user_model()


@pytest.mark.django_db
def test_signup_success(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.first().is_active is False
    assert User.objects.first().first_name == signup_body['first_name']
    assert 'confirm_code_id' in response.data
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_signup_with_empty_body(client, signup_url):
    response = client.post(signup_url, data=dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_signup_email_already_in_use(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_signup_success_without_patronymic(client, signup_url, signup_body):
    signup_body.pop('patronymic')
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_signup_success_with_empty_patronymic(client, signup_url, signup_body):
    signup_body['patronymic'] = ''
    response = client.post(signup_url, data=signup_body)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_confirm_code_success(
    client,
    signup_url,
    signup_body
):
    response = client.post(signup_url, data=signup_body)
    confirm_code_id = response.data['confirm_code_id']
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    response = client.post(reverse('users:confirm_code', args=(code, confirm_code_id)))
    assert response.status_code == status.HTTP_200_OK
    assert User.objects.first().is_active is True


@pytest.mark.django_db
@pytest.mark.usefixtures('active_user')
def test_signup_already_active(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    assert User.objects.count() == 1
    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.django_db
def test_confirm_code_wrong_code(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    confirm_code_id = response.data['confirm_code_id']
    response = client.post(reverse('users:confirm_code', args=('314921', confirm_code_id)))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_confirm_code_wrong_format_of_code_id(client, signup_url, signup_body):
    client.post(signup_url, data=signup_body)
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    response = client.post(reverse('users:confirm_code', args=(code, '5179fh91')))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_confirm_code_code_id_not_exist(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    confirm_code_id = response.data['confirm_code_id']
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    response = client.post(reverse('users:confirm_code', args=(code, confirm_code_id[::-1])))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_confirm_code_code_expired(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    confirm_code_id = response.data['confirm_code_id']
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    session = SignupSession.objects.first()
    session.expiration_time = timezone.now() - timezone.timedelta(minutes=5)
    session.save()
    response = client.post(reverse('users:confirm_code', args=(code, confirm_code_id)))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_updated_user_after_new_confirm_code(
    client,
    signup_url,
    signup_body
):
    new_first_name = 'аоыда'
    new_last_name = 'афдодф'
    client.post(signup_url, data=signup_body, content_type='application/json')
    updated_body = signup_body.copy()
    updated_body['first_name'] = new_first_name
    updated_body['last_name'] = new_last_name
    client.post(signup_url, data=updated_body, content_type='application/json')

    user = User.objects.all().first()
    assert user.first_name == new_first_name
    assert user.last_name == new_last_name
    assert user.patronymic == signup_body['patronymic']


@pytest.mark.django_db
def test_double_reg(
    client,
    signup_url,
):
    test_body = {
        "email": "rqo70851@zccck.com",
        "password": "jgjkdf+Hj8",
        "repeat_password": "jgjkdf+Hj8",
        "first_name": "Андрияна",
        "last_name": "Петрова",
        "patronymic": "Олеговна",
        "secret_word": "словушко"
    }
    client.post(signup_url, data=test_body, content_type='application/json')
    response = client.post(signup_url, data=test_body, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
