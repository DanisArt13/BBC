from django.contrib import admin
from .models import User  # Импортируйте вашу модель пользователя

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')  # Поля для отображения в списке
    search_fields = ('username', 'email')  # Поисковые поля
    list_filter = ('is_active', 'is_staff')  # Фильтрация

admin.site.register(User, UserAdmin)  # Регистрация модели в админке