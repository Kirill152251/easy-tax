from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import FileExtensionValidator
from django.db import models

from core import const
from core.models import BaseModel


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email not provided')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


def avatar_upload_to(instance, filename):
    return 'users_avatars/{0}/{1}'.format(instance.id, filename)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField('Адрес электронной почты', unique=True)
    first_name = models.CharField('Имя', max_length=const.FIRST_NAME_MAX_LEN)
    last_name = models.CharField('Фамилия', max_length=const.LAST_NAME_MAX_LEN)
    patronymic = models.CharField(
        'Отчество',
        max_length=const.PATRONYMIC_MAX_LEN,
        blank=True,
        null=True
    )
    unp = models.CharField(
        'Учетный номер плательщика',
        max_length=const.PAYER_ACCOUNT_NUMBER_MAX_LEN,
        blank=True,
        null=True
    )
    registration_address = models.CharField(
        'Адрес регистрации',
        max_length=const.ADDRESS_MAX_LEN,
        blank=True,
        null=True
    )
    residential_address = models.CharField(
        'Адрес проживания',
        max_length=const.ADDRESS_MAX_LEN,
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    date_of_birth = models.DateField(blank=True, null=True)
    secret_word = models.CharField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserProfileManager()

    @property
    def is_npd_payer(self):
        return bool(self.unp)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'User(email={self.email}, is_active={self.is_active})'


class SignupSession(BaseModel):
    email = models.EmailField()
    confirm_code = models.PositiveIntegerField()
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f'SighupSession(email={self.email}, confirm_code={self.confirm_code})'
