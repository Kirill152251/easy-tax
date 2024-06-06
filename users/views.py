import datetime
from random import randint

from drf_spectacular.utils import extend_schema, inline_serializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import RegistrationSession


User = get_user_model()


class RegistrationView(CreateAPIView):
    """
    Сохраняет пользователя в неактивном состоянии и отравляет на
    его почту письмо с кодом подтверждения.
    При успешном выполнении возвращает id кода подтверждения, 
    который нужен будет, что бы активировать пользователя и 
    закончить его регистрацию. Если пользователь с указаным в запросе
    email уже активирован - вернет 202. 
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        tags=['Registration'],
        responses={
            201: inline_serializer(
                name='SignupResponse',
                fields={
                    'confirm_code_id': serializers.IntegerField(),
                }
            ),
            202: None,
        }
    )
    def post(self, request):
        email = request.get('username')
        if not User.objects.filter(username=email).exist():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            is_active = User.objects.get(username=email).is_active
            if is_active:
                return Response(status=status.HTTP_202_ACCEPTED)

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


@extend_schema(tags=['Registration'])
@api_view(['POST'])
def confirm_code(request):
    code = request.query_params['code']
    code_id = request.query_params['code_id']

    session = get_object_or_404(RegistrationSession, pk=code_id) 
    if session.confirm_code != code:
        #TODO: return appropriate response
        pass
    if datetime.datetime.now() > session.expiration_time:
        #TODO: return appropriate response
        pass
    user = User.objects.get(username=session.email)
    user.is_active = True
    user.save()
    return Response(status=status.HTTP_200_OK)

