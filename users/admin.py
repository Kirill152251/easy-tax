from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {'fields': [
                'email',
                'first_name',
                'last_name',
                'patronymic',
                'is_active',
                'is_admin',
                'unp',
                'registration_address',
                'residential_address',
                'avatar',
                'date_of_birth',
            ]}
        ),
    )
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'unp', 'is_active')
    readonly_fields = ('id', 'created_at')


admin.site.register(User, CustomUserAdmin)
