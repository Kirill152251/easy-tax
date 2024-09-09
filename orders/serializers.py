from rest_framework import serializers

from orders.models import Order

from products.serializers import ProductSerializer
from users.serializers import UserGetSerializer


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'product', 'count', 'seller', 'buyer', 'created_at')


class OrderGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    buyer = UserGetSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'product', 'buyer', 'created_at')
