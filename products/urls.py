from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductImageViewSet, ProductViewSet


router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
