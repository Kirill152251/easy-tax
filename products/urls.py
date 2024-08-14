from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductImageViewSet, ProductViewSet


router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
