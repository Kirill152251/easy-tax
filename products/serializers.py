import os

from rest_framework import serializers
from .models import ProductCategory, Product, ProductImage


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductImageSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=200)

    class Meta:
        model = ProductImage
        fields = ('id', 'photo', 'product')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if str(os.getenv('DEBUG', default='1')) == '0':
            ret['photo'] = os.getenv('BASE_SERVER_URL') + instance.photo.url
        return ret


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'count', 'category', 'seller', 'images',)
