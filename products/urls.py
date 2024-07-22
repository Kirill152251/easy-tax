from django.urls import path
from .views import (
    ProductCategoryListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductImageListAPIView,
    ProductImageDetailAPIView,
)


app_name = 'products'

urlpatterns = [
    # Маршруты для ProductCategory
    path('categories/', ProductCategoryListAPIView.as_view(), name='product-category-list'),

    # Маршруты для Product
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),

    # Маршруты для ProductImage
    path('product-images/', ProductImageListAPIView.as_view(), name='product-image-list'),
    path('product-images/<int:pk>/', ProductImageDetailAPIView.as_view(), name='product-image-detail'),
]
