from .models import ProductCategory, Product, ProductImage
from .serializers import (
                        ProductCategorySerializer,
                        ProductSerializer,
                        ProductImageSerializer,
                        )
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    @extend_schema(
        description="Get a list of product categories.",
        responses={200: "List of product categories"},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    