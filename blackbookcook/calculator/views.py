from django.views import View
from django.shortcuts import render
from dishes.models import Dish
from products.models import Product

class CalculatorView(View):
    template_name = 'calculator/calculator.html'

    def get(self, request):
        products_list = Product.objects.all()
        dish_list = Dish.objects.all()
        
        return render(request, self.template_name, {
            'products': products_list,
            'dishes': dish_list,
        })
