from django.shortcuts import render
from rest_framework import generics
from .models import ProductCategory, Product, ProductImage
from .serializers import (
                        ProductCategorySerializer,
                        ProductSerializer,
                        ProductImageSerializer,
                        )


class ProductCategoryListAPIView(generics.ListAPIView):
    """
    API-представление для получения списка категорий товаров.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductListAPIView(generics.ListCreateAPIView):
    """
    API-представление для получения списка товаров или создания нового товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API-представление для получения, обновления или удаления товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageListAPIView(generics.ListCreateAPIView):
    """
    API-представление для получения списка изображений товаров или создания нового изображения.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API-представление для получения, обновления или удаления изображения товара.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    