from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'patronymic',
            'payer_account_number'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic'],
            is_active=False,
            payer_account_number=validated_data['payer_account_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    #TODO: implement password validation
    

    def validate_username(self, value):
        if User.objects.filter(username=value).exist():
            raise serializers.ValidationError(
                'Email is already taken'
            )
        return value

    def validate_payer_account_number(self, value):
        if User.objects.filter(payer_account_number=value).exist():
            raise serializers.ValidationError(
                'Payer account number is already taken'
            )
        return value

