import os
from random import randint

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from core.const import CONFIRM_CODE_EXPIRATION_TIME_MIN
from core.permissions import IsActive
from easy_tax_api.serializers import DetailSerializer
from users.serializers import (
    SignupSerializer,
    UserGetSerializer,
    UpdateUserSerializer,
    UploadAvatarSerializer,
    ConfirmCodeIDSerializer,
)
from products.serializers import ProductSerializer
from orders.serializers import OrderGetSerializer
from users.models import SignupSession


User = get_user_model()


class SignupAPIView(generics.CreateAPIView):
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
    permission_classes = [AllowAny]

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        if not User.objects.filter(email=email).exists():
            self.perform_create(serializer)
        else:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                user.delete()
                self.perform_create(serializer)

        conf_code = randint(100000, 999999)
        session = SignupSession(
            confirm_code=conf_code,
            email=email,
            expiration_time=timezone.now() + timezone.timedelta(minutes=CONFIRM_CODE_EXPIRATION_TIME_MIN)
        )
        session.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код: {conf_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return Response(
            ConfirmCodeIDSerializer(session).data,
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=['Signup'],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=UserGetSerializer,
            description='Пользователь активирован успешно.'
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=DetailSerializer,
            description='Если неправельный код подтверждения: {"details": "wrong code"}. '
                        'Если срок действия кода истек: {"details": "code expired"}.'
                        'Если неправильный формат confirm_code_id: {"details": "incorrect confirm_code_id"}.'
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
    try:
        session = get_object_or_404(SignupSession, pk=confirm_code_id)
    except ValidationError:
        return Response(
            DetailSerializer({'details': 'incorrect confirm_code_id'}).data,
            status=status.HTTP_400_BAD_REQUEST
        )

    if session.confirm_code != code:
        return Response(
            DetailSerializer({'details': 'wrong code'}).data,
            status=status.HTTP_400_BAD_REQUEST
        )

    if timezone.now() > session.expiration_time:
        return Response(
            DetailSerializer({'details': 'code expired'}).data,
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.get(email=session.email)
    user.is_active = True
    user.save()
    return Response(data=UserGetSerializer(user).data, status=status.HTTP_200_OK)


class UserGetUpdateAPIView(APIView):
    permission_classes = [IsActive]

    @extend_schema(
        tags=['User me'],
        responses=UserGetSerializer
    )
    def get(self, request):
        """
        Получение данных аутентифицированного пользователя. Права доступа:
        аутентифицированный активный пользователь.
        """
        return Response(UserGetSerializer(request.user).data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['User me'],
        responses=UserGetSerializer,
        request=UpdateUserSerializer
    )
    def patch(self, request):
        """
        Изменение данных аутентифицированного пользователя. Права доступа:
        аутентифицированный активный пользователь.
        """
        serializer = UpdateUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserGetSerializer(request.user).data, status=status.HTTP_200_OK)


class UserAvatarAPIView(APIView):
    permission_classes = [IsActive]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=['User me'],
        responses=UserGetSerializer,
        request=UploadAvatarSerializer
    )
    def post(self, request):
        """
        Установка/обновление аватара пользователя. Права доступа:
        аутентифицированный активный пользователь.
        """
        serializer = UploadAvatarSerializer(
            request.user,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserGetSerializer(request.user).data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['User me'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(response=UserGetSerializer)
        }
    )
    def delete(self, request):
        """
        Удаление аватара пользователя. Права доступа:
        аутентифицированный активный пользователь.
        """
        user = request.user
        user.avatar.delete()
        return Response(UserGetSerializer(request.user).data, status=status.HTTP_200_OK)


@extend_schema(tags=['User me'])
class UserProductsListAPIView(generics.ListAPIView):
    """
    Получение всех продуктов пользователя. Права доступа:
    аутентифицированный активный пользователь.
    """
    permission_classes = [IsActive]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.products.all()


@extend_schema(tags=['User me'])
class UserOrdersListAPIView(generics.ListAPIView):
    """
    Получение заказов пользователя. Права доступа:
    аутентифицированный активный пользователь.
    """
    permission_classes = [IsActive]
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return self.request.user.orders_to_sell.all()


@extend_schema(tags=['User me'])
@api_view(['GET'])
@permission_classes([IsActive])
def get_orders_sum(request):
    """
    Получение суммы стоимсти всех заказов пользователь.
    Пример ответа: {"sum": 720.42}.
    Права доступа: аутентифицированный активный пользователь.
    """
    orders = request.user.orders_to_sell.all()
    sum = 0
    for order in orders:
        sum += order.count * order.product.price
    return Response({'sum': sum})
