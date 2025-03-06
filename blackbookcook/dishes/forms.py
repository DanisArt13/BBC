from django import forms
from .models import Dish, Product, RecipeIngredient, UserCreatedDish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'recipes']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['product', 'weight']