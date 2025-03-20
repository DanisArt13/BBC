from django.views import View
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

class ProductsView(View):
    def get(self, request):
        form = ProductForm()
        products_list = Product.objects.all()
        categories = Product.objects.values_list('categories', flat=True).exclude(categories='').distinct()
        print(categories)
        return render(request, 'products/products.html', {'form': form, 'products': products_list, 'categories': categories})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:products')  # Перенаправление на ту же страницу
        products_list = Product.objects.all()
        return render(request, 'products/products.html', {'form': form, 'products': products_list})
