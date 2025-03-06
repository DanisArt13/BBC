from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import SmallAutoField, DecimalField, CharField, ImageField, TextField, ForeignKey, ManyToManyField
from products.models import Product
from users.models import User
# Модель Dish
class Dish(models.Model):
    name = CharField(max_length=50, unique=True)
    images = ImageField(upload_to='dishes/images', null=True, blank=True)
    recipes = TextField(null=True)
    proteins = DecimalField(max_digits=5, decimal_places=2)
    fats = DecimalField(max_digits=5, decimal_places=2)
    carbs = DecimalField(max_digits=5, decimal_places=2)
    kcals = DecimalField(max_digits=5, decimal_places=2)
    categorys = CharField(max_length=50, null=True)
    areas = CharField(max_length=50, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'dishes'

    def __repr__(self):
        return f'{self.name}\n{self.kcals}\n{self.proteins}\n{self.fats}\n{self.carbs}'
 
# Модель RecipeIngredient
class RecipeIngredient(models.Model):
    dish = ForeignKey(Dish, related_name='ingredients', on_delete=models.CASCADE)
    product = ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.FloatField()  # вес продукта в граммах

    class Meta:
        db_table = 'dishes_products'
    
    def __str__(self):
        return f"{self.product.name} in {self.dish.name} - {self.weight}g"

    def __repr__(self):
        return f"{self.product.name} - {self.weight}g" 

class UserDish(models.Model):
    user = ForeignKey(User, related_name='user_dishes', on_delete=models.CASCADE)
    dish = ForeignKey(Dish, related_name='user_dishes', on_delete=models.CASCADE)  # Укажите правильный путь к модели Dish
    ingredients = ManyToManyField('dishes.RecipeIngredient', blank=True)  # Укажите правильный путь к модели RecipeIngredient catalog

    class Meta:
        db_table = 'user_dishes'

    def __repr__(self):
        return f"{self.user.username}'s dish: {self.dish.name}"

def user_dish_image_path(instance, filename):
    return f'users/{instance.user.id}/user_dish_image/{filename}'

class UserCreatedDish(models.Model):
    user = models.ForeignKey(User, related_name='user_created_dishes', on_delete=models.CASCADE)  # Связь с пользователем
    name = models.CharField(max_length=50)  # Название блюда
    images = models.ImageField(upload_to=user_dish_image_path, null=True, blank=True)  # Путь к изображению
    category = models.CharField(max_length=50, null=True)
    recipes = models.TextField(null=True)  # Рецепт блюда
    products = models.ManyToManyField(Product, blank=True)  # Укажите правильный путь к модели Product

    class Meta:
        db_table = 'user_created_dishes'

    def __repr__(self):
        return f"{self.user.username}'s created dish: {self.name}"

class UserCreatedDishProduct(models.Model):
    dish = models.ForeignKey(UserCreatedDish, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.FloatField()  # Дополнительное поле, например, для веса

    class Meta:
        db_table = 'user_created_dish_products'
        unique_together = ('dish', 'product')