from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from users.const import (PAYER_ACCOUNT_NUMBER_MAX_LEN, FIRST_NAME_MAX_LEN,
                         LAST_NAME_MAX_LEN, PATRONYMIC_MAX_LEN, SECRETWORD_MAX_LEN)


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email not provided')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField('Адрес электронной почты', unique=True)
    first_name = models.CharField('Имя', max_length=FIRST_NAME_MAX_LEN)
    last_name = models.CharField('Фамилия', max_length=LAST_NAME_MAX_LEN)
    patronymic = models.CharField('Отчество', max_length=PATRONYMIC_MAX_LEN, blank=True)
    payer_account_number = models.CharField(
        'Учетный номер плательщика',
        max_length=PAYER_ACCOUNT_NUMBER_MAX_LEN,
        blank=True
    )
    secret_word = models.CharField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserProfileManager()

    class Meta:
        ordering = ('email',)

    def __str__(self):
        return f'User(id={self.id}, email={self.email})'


class SignupSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField()
    confirm_code = models.PositiveIntegerField()
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f'SighupSession(email={self.email}, confirm_code={self.confirm_code})'
