from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from products.models import ProductCategory, Product, ProductImage
from products.serializers import (
    ProductCategorySerializer,
    ProductSerializer,
    ProductImageSerializer,
)


@extend_schema(tags=['Product Categoty'])
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


@extend_schema(tags=['Product Image'])
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=['Product'])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
