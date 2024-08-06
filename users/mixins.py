import re

from django.contrib.auth import get_user_model
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core import const


User = get_user_model()


class UserValidationMixin(metaclass=serializers.SerializerMetaclass):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        min_length=const.FIRST_NAME_MIN_LEN,
        max_length=const.FIRST_NAME_MAX_LEN,
        trim_whitespace=False
    )
    last_name = serializers.CharField(
        min_length=const.LAST_NAME_MIN_LEN,
        max_length=const.LAST_NAME_MAX_LEN,
        trim_whitespace=False
    )
    patronymic = serializers.CharField(
        min_length=const.PATRONYMIC_MIN_LEN,
        max_length=const.PATRONYMIC_MAX_LEN,
        required=False,
        allow_blank=True,
        trim_whitespace=False
    )

    def fio_validation(self, string, error_msg):
        if (
            re.fullmatch(pattern=const.FIO_REGEX, string=string) is None or
            '--' in string or
            string == '-'
        ):
            raise serializers.ValidationError(error_msg)

    def validate_first_name(self, value):
        self.fio_validation(value, 'Invalid first name')
        return value

    def validate_last_name(self, value):
        self.fio_validation(value, 'Invalid last name')
        return value

    def validate_patronymic(self, value):
        if value == '':
            return None
        self.fio_validation(value, 'Invalid patronymic')
        return value

    def validate_email(self, value):
        try:
            email = value.lower()
            email_info = validate_email(email, check_deliverability=True)
            return email_info.normalized
        except EmailNotValidError as e:
            raise serializers.ValidationError(e)
