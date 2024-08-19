import re
from typing import Any

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from passlib.context import CryptContext

from core import const
from users.mixins import UserValidationMixin
from users.models import SignupSession


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
            'passport_num',
            'phone_number',
            'date_of_birth',
        )

    def validate_residential_address(self, validated_data):
        if re.fullmatch(pattern=const.ADDRESS_REGEX, string=validated_data) is None:
            raise serializers.ValidationError('Invalid registration address')
        return validated_data

    def validate_registration_address(self, validated_data):
        if re.findall(pattern=const.ADDRESS_REGEX, string=validated_data) is None:
            raise serializers.ValidationError('Invalid registration address')
        return validated_data

    def validate_date_of_birth(self, validated_data):
        if validated_data > timezone.now().date():
            raise serializers.ValidationError('Date of birth cannot be in future')
        if timezone.now().date() - validated_data > timezone.timedelta(days=360 * 120):
            raise serializers.ValidationError('The date is too old')
        return validated_data

    def validate_unp(self, validated_data):
        if re.fullmatch(pattern=r'[A-Z]{9}', string=validated_data):
            raise serializers.ValidationError('Invalid unp')
        if re.fullmatch(pattern=const.UNP_REGEX, string=validated_data) is None:
            raise serializers.ValidationError('Invalid unp')
        return validated_data

    def validate_phone_number(self, validated_data):
        if re.fullmatch(pattern=const.PHONE_NUMBER_REGEX_BY, string=validated_data) is None:
            raise serializers.ValidationError('Invalid phone number')
        return validated_data

    def validate_passport_num(self, validated_data):
        if re.fullmatch(pattern=const.PASSPORT_NUM_REGEX, string=validated_data) is None:
            raise serializers.ValidationError('Invalid passport number')
        return validated_data


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
            'passport_num',
            'phone_number',
            'avatar'
        )


class ConfirmCodeIDSerializer(serializers.ModelSerializer):
    confirm_code_id = serializers.UUIDField(read_only=True, source='id')

    class Meta:
        model = SignupSession
        fields = ('confirm_code_id',)


class SignupSerializer(UserValidationMixin, serializers.ModelSerializer):
    email = serializers.EmailField()
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


class EmailLowercaseTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        try:
            email_lowercase = attrs[self.username_field].lower()
            attrs[self.username_field] = email_lowercase
        except AttributeError:
            pass
        return super().validate(attrs)
