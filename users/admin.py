from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from products.models import ProductCategory, Product, ProductImage

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {'fields': ['email', 'first_name', 'last_name', 'patronymic', 'is_active']}
        ),
    )
    ordering = ('email',)
    list_display = ('email',)


admin.site.register(User, CustomUserAdmin)

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
    ordering = ( '-category', '-seller',)
    list_per_page = 25


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('avatar', 'product',)
    list_filter = ('avatar', 'product',)
    search_fields = ('avatar', 'product',)
    ordering = ('avatar', 'product',)
    readonly_fields = ('avatar', 'product',)
    list_per_page = 10
