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
