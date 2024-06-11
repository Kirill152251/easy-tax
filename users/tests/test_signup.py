from django.urls import reverse
import pytest
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
    assert User.objects.first().is_active == False
    assert 'confirm_code_id' in response.data
    assert len(mail.outbox) == 1


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
    assert User.objects.first().is_active == True 


@pytest.mark.django_db
def test_signup_already_active(client, active_user, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    assert User.objects.count() == 1
    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.django_db
def test_confirm_code_wrong_code(client, signup_url, signup_body):
    response = client.post(signup_url, data=signup_body)
    confirm_code_id = response.data['confirm_code_id']
    email_massage = mail.outbox[0].body
    code = ''.join(d for d in email_massage if d.isdigit())
    response = client.post(reverse('users:confirm_code', args=('314921', confirm_code_id)))
    assert response.status_code == status.HTTP_400_BAD_REQUEST 
    assert response.data['details'] == 'wrong code'
    

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
    assert response.data['details'] == 'code expired'

