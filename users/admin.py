from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """Кастомный админ-класс для модели User"""

    # Поля для отображения в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')

    # Поля для фильтрации
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')

    # Группировка полей при редактировании
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Роли и права', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'password1', 'password2', 'role'),
        }),
    )

    # Поля для поиска
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Сортировка по умолчанию
    ordering = ('-date_joined',)

    # Поля только для чтения
    readonly_fields = ('last_login', 'date_joined')

    # Методы для отображения в списке
    def get_role_display(self, obj):
        """Отображаем человекочитаемое название роли"""
        return dict(User.ROLE_CHOICES).get(obj.role, obj.role)

    get_role_display.short_description = 'Роль'


# Регистрируем модель с кастомным админ-классом
admin.site.register(User, CustomUserAdmin)