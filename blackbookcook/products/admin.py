from django.contrib import admin
from .models import Product
from django import forms  # Импортируем forms, если вы хотите использовать их

# Убедитесь, что вы импортировали необходимые классы

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'fats', 'proteins', 'carbohydrates', 'water', 'sugar', 'image_url', 'categories', 'text', 'area')  # Поля, отображаемые в списке
    search_fields = ('name',)  # Позволяет искать по названию продукта
    list_filter = ('categories',)  # Фильтры по категориям
    ordering = ('name',)  # Сортировка по имени
    
    fieldsets = (
        (None, {
            'fields': ('name', 'calories', 'fats', 'proteins', 'carbohydrates', 'water', 'sugar', 'image_url', 'categories', 'text', 'area'),
        }),
    )


    # Убедитесь, что вы правильно ссылаетесь на модели
    formfield_overrides = {
        forms.ImageField: {
            'widget': admin.widgets.AdminFileWidget(),  # Используем специальный виджет для загрузки изображений
        },
    }

# Регистрация модели
admin.site.register(Product, ProductAdmin)
