import datetime
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import RegistrationSession


User = get_user_model()


class RegistrationView(CreateAPIView):
    """
    Save new inactive user. After addressing to this endpoint
    email with comfirmation code will be send to user email. Return
    confirmation code id, that will be needed to approve code and
    activate user. If user already activated, return:
    {'message': 'User already activated'}
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        email = request.get('email')
        if not User.objects.filter(username=email).exist():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            is_active = User.objects.get(username=email).is_active
            if is_active:
                return Response({'message': 'User already activated'}, status=status.HTTP_200_OK)

        conf_code = randint(100000, 999999)
        session = RegistrationSession(
            conf_code=conf_code,
            email=email,
            expiration_time=datetime.datetime.now() + datetime.timedelta(minutes=1)
        )
        session.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код: {conf_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

        return Response({'confirm_code_id': session.id}, status=status.HTTP_200_OK)

