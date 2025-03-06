from django.views import View
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

class ProductsView(View):
    def get(self, request):
        form = ProductForm()
        products_list = Product.objects.all()
        return render(request, 'products/products.html', {'form': form, 'products': products_list})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:products')  # Перенаправление на ту же страницу
        products_list = Product.objects.all()
        return render(request, 'products/products.html', {'form': form, 'products': products_list})
