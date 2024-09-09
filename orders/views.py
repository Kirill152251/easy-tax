from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from core.permissions import IsActive
from orders.models import Order
from orders.serializers import OrdersSerializer


@extend_schema(
    tags=['Orders'],
    description="""
        Права доступа: аутентифицированный активный пользователь.
    """
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsActive]
