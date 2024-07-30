import os
import re

from django.contrib.auth import get_user_model
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from passlib.context import CryptContext

from core import const
from users.mixins import UserValidationMixin


User = get_user_model()
pwd_context = CryptContext(schemes=['bcrypt'])


class UpdateUserSerializer(
    UserValidationMixin,
    serializers.ModelSerializer,
):
    registration_address = serializers.CharField(
        max_length=const.ADDRESS_MAX_LEN,
    )
    residential_address = serializers.CharField(
        max_length=const.ADDRESS_MAX_LEN,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'unp',
            'registration_address',
            'residential_address',
            'date_of_birth',
        )


class UploadAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=200)

    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'unp',
            'registration_address',
            'residential_address',
            'date_of_birth',
            'avatar'
        )


class SignupSerializer(UserValidationMixin, serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=const.PASSWORD_MIN_LEN,
        max_length=const.PASSWORD_MAX_LEN,
        write_only=True,
        trim_whitespace=False
    )
    secret_word = serializers.CharField(
        min_length=const.SECRETWORD_MIN_LEN,
        max_length=const.SECRETWORD_MAX_LEN,
        write_only=True,
        trim_whitespace=False
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'patronymic',
            'secret_word'
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data.get('patronymic', None),
        )
        user.set_password(validated_data['password'])
        user.secret_word = pwd_context.hash(validated_data['secret_word'])
        user.save()
        return user

    def validate_secret_word(self, validated_data):
        chars_check = re.fullmatch(r'[а-яА-яЁё]+', validated_data)
        if chars_check is None:
            raise serializers.ValidationError('Ivalid secret word')
        return validated_data

    def validate_password(self, validated_data):
        chars_check = re.fullmatch(r'[a-zA-Z0-9_!@#$%^&*()+-:;,.]+', validated_data)
        uppercase_check = re.search(r'[A-Z]', validated_data)
        lowercase_check = re.search(r'[a-z]', validated_data)
        digits_check = re.search(r'\d', validated_data)
        repeats_check = re.search(r'(.)\1{2}', validated_data)
        if (
            chars_check is None or
            uppercase_check is None or
            lowercase_check is None or
            digits_check is None or
            repeats_check is not None
        ):
            raise serializers.ValidationError('Invalid password')
        return validated_data
