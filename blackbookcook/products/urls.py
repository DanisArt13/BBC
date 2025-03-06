""" Продукты """

from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsView.as_view(), name='products'),  # URL для входа
]