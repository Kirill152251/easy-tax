from django.contrib.auth.models import AbstractUser
from django.db import models

from users.const import PAYER_ACCOUNT_NUMBER_MAX_LEN


class UserProfile(AbstractUser):
    username = models.EmailField('Адрес электронной почты', unique=True)
    first_name = models.CharField('Имя', max_length=150),
    last_name = models.CharField('Фамилия', max_length=150),
    patronymic = models.CharField('Отчество', max_length=150),
    payer_account_number = models.CharField(
        'Учетный номер плательщика',
        max_length=PAYER_ACCOUNT_NUMBER_MAX_LEN
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return f'User(id={self.id}, email={self.username})'
    

class RegistrationSession(models.Model):
    email = models.EmailField()
    confirm_code = models.PositiveIntegerField()
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f'RegistrationSessin(email={self.email}, confirm_code={self.confirm_code})'

