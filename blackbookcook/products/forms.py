from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'calories', 'fats', 'proteins', 'carbohydrates', 'water', 'sugar', 'image_url', 'categories', 'text', 'area']