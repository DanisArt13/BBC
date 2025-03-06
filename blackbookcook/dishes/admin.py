from django.contrib import admin
from dishes.models import Dish, RecipeIngredient
from products.models import Product
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Количество пустых форм для добавления новых продуктов

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    inlines = [RecipeIngredientInline]
    
    # Включите опции для удаления объектов
    def has_delete_permission(self, request, obj=None):
        return True  # Позволяет удалять объекты

    def delete_model(self, request, obj):
        obj.delete()  # Удаление объекта при подтверждении
