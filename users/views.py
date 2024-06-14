from random import randint

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiExample
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from easy_tax_api.serializers import DetailSerializer
from users.serializers import SignupSerializer, UserSerializer
from users.models import SignupSession


User = get_user_model()


class SignupAPIView(CreateAPIView):
    """
    Сохраняет пользователя в неактивном состоянии и отравляет на
    его почту письмо с кодом подтверждения.
    При успешном выполнении возвращает id кода подтверждения, 
    который нужен будет, что бы активировать пользователя и 
    закончить его регистрацию. Если пользователь с указаным в запросе
    email уже активирован - вернет 202. В теле запроса все поля кроме
    отчества обязательны.
    """

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]

    @extend_schema(
        tags=['Signup'],
        request=SignupSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Неактивный пользователь cохранен, письмо отправлено.",
                response=inline_serializer(
                    name='SignupResponse',
                    fields={
                        'confirm_code_id': serializers.CharField(),
                    }
                )
            ),
            status.HTTP_202_ACCEPTED: OpenApiResponse(
                description='Пользователь уже активирован.'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Ошибка валидации.' 
            )
        }
    )
    def post(self, request):
        email = request.data['email']
        if not User.objects.filter(email=email).exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            is_active = User.objects.get(email=email).is_active
            if is_active:
                return Response(status=status.HTTP_202_ACCEPTED)

        conf_code = randint(100000, 999999)
        session = SignupSession(
            confirm_code=conf_code,
            email=email,
            expiration_time=timezone.now() + timezone.timedelta(minutes=1)
        )
        session.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код: {conf_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return Response({'confirm_code_id': str(session.id)}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Signup'],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=UserSerializer,
            description='Пользователь активирован успешно.'
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=DetailSerializer,
            description='Если неправельный код подтверждения: {"details": "wrong code"}. ' 
                        'Если срок действия кода истек: {"details": "code expired"}.'
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description='Несуществующий code_id.'
        ) 
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_code(request, code, confirm_code_id):
    """
    Через параметры запроса получает код подверждения и его id
    (см. /api/v1/singup/) и заканчивает регистрацию, активируя пользователя.
    """
    session = get_object_or_404(SignupSession, pk=confirm_code_id) 

    if session.confirm_code != code:
        return Response(
            DetailSerializer({'details':'wrong code'}).data,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if timezone.now() > session.expiration_time:
        return Response(
            DetailSerializer({'details':'code expired'}).data,
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.get(email=session.email)
    user.is_active = True
    user.save()
    return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

