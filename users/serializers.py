import re
from django.contrib.auth import get_user_model
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from passlib.context import CryptContext

from users import const


User = get_user_model()
pwd_context = CryptContext(schemes=['bcrypt'])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
        )



class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        min_length=const.FIRST_NAME_MIN_LEN,
        max_length=const.FIRST_NAME_MAX_LEN
    )
    last_name = serializers.CharField(
        min_length=const.LAST_NAME_MIN_LEN,
        max_length=const.LAST_NAME_MAX_LEN
    )
    patronymic = serializers.CharField(
        min_length=const.PATRONYMIC_MIN_LEN,
        max_length=const.PATRONYMIC_MAX_LEN,
        required=False
    )
    password = serializers.CharField(
        min_length=const.PASSWORD_MIN_LEN,
        max_length=const.PASSWORD_MAX_LEN
    )
    secret_word = serializers.CharField(
        min_length=const.SECRETWORD_MIN_LEN,
        max_length=const.SECRETWORD_MAX_LEN
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
            'password': {'write_only': True},
            'secret_word': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic'],
        )
        user.set_password(validated_data['password'])
        user.secret_word = pwd_context.hash(validated_data['secret_word'])
        user.save()
        return user
    
    def validate_secret_word(self, validated_data):
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        if highpoints.search(validated_data) != None:
            raise serializers.ValidationError('Secret word must not contain emoji')
        return validated_data

    def validate_password(self, validated_data):
        chars_check = re.fullmatch(r'[a-zA-Z0-9_!@#$%^&*()+-:;,.]+', validated_data)
        capital_check = re.search(r'[A-Z]', validated_data)
        digits_check = re.search(r'\d', validated_data)
        repeats_check = re.search(r'(.)\1{2}', validated_data)
        if chars_check == None or capital_check == None or digits_check == None or repeats_check != None:
            raise serializers.ValidationError('Invalid password')
        return validated_data

    def validate_first_name(self, validated_data):
        if not re.fullmatch(pattern=const.FIO_REGEX, string=validated_data):
            raise serializers.ValidationError('Invalid first name')
        return validated_data

    def validate_last_name(self, validated_data):
        if not re.fullmatch(pattern=const.FIO_REGEX, string=validated_data):
            raise serializers.ValidationError('Invalid last name')
        return validated_data

    def validate_patronymic(self, validated_data):
        if not re.fullmatch(pattern=const.FIO_REGEX, string=validated_data):
            raise serializers.ValidationError('Invalid patronymic')
        return validated_data

    def validate_email(self, validated_data):
        try:
            email_info = validate_email(validated_data, check_deliverability=True)
            return email_info.normalized
        except EmailNotValidError as e:
                raise serializers.ValidationError(e)

