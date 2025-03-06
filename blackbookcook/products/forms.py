from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'images', 'text', 'proteins', 'fats', 'carbs', 'kcals', 'categorys', 'areas']