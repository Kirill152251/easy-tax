from django.contrib import admin
from products.models import ProductCategory, Product, ProductImage


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 25


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'count', 'category', 'seller',)

    list_filter = ('name', 'description', 'price', 'count', 'category', 'seller',)
    search_fields = ('name', 'category', 'seller',)
    ordering = ('-category', '-seller',)
    list_per_page = 25


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('photo', 'product',)
    list_filter = ('photo', 'product',)
    search_fields = ('photo', 'product',)
    ordering = ('photo', 'product',)
    readonly_fields = ('photo', 'product',)
    list_per_page = 10
