""" Калькулятор """
from django.urls import path
from calculator import views

app_name = 'calculator'

urlpatterns = [
    path('', views.CalculatorView.as_view(), name='calculator'), 
]