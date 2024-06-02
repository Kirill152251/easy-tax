from django.contrib.auth.models import AbstractUser
from django.db import models

from users.const import PAYER_ACCOUNT_NUMBER_MAX_LEN


class UserProfile(AbstractUser):
    """Custom User model."""

    username = models.EmailField('Адрес электронной почты', unique=True)
    payer_account_number = models.CharField(
        'Учетный номер плательщика',
        max_length=PAYER_ACCOUNT_NUMBER_MAX_LEN
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return f'User(id={self.id}, email={self.username})'
    

