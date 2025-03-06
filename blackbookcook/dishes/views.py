from django.views.generic import ListView
from . import models
from django.test import TestCase
from django.urls import reverse
from .models import Dish, UserDish
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

class DishView(ListView):
    model = models.Dish
    template_name = 'dishes/dishes.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        dishes_list = self.model.objects.prefetch_related('ingredients__product').all()
        for dish in dishes_list:
            dish.ingredients_list = ', '.join([
                f"{ingredient.product.name}: {ingredient.weight} гр." for ingredient in dish.ingredients.all()
            ])
        return dishes_list

    def post(self, request, *args, **kwargs):
        # Пример: добавление нового блюда или выполнение других действий
        # Здесь может быть логика обработки формы, аналогично ProductsView
        # Например, если есть форма для добавления нового блюда:
        # form = DishForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('dishes:index')  # Переход на список блюд

        return redirect('dishes:index')  

class AddUserDishView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        dish_id = request.POST.get('dish_id')  # Получаем ID блюда
        
        if dish_id is None:
            return HttpResponseRedirect(reverse('dishes'))

        try:
            dish = Dish.objects.get(id=int(dish_id))
            # Проверка, существует ли запись для текущего пользователя и блюда
            if not UserDish.objects.filter(user=request.user, dish=dish).exists():
                UserDish.objects.create(user=request.user, dish=dish)
                messages.success(request, 'Рецепт успешно добавлен!')  # Сообщение об успешном добавлении
            else:
                messages.warning(request, 'Этот рецепт уже добавлен!')  # Сообщение, что рецепт уже существует

        except Dish.DoesNotExist:
            return HttpResponseRedirect(reverse('dishes:dishes'))

        # Перенаправляем на ту же страницу с блюдами
        return HttpResponseRedirect(reverse('dishes:dishes'))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dishes:dishes'))
        
class SavedDishesView(LoginRequiredMixin, View):
    template_name = 'dishes/saved_dishes.html'

    def get(self, request):
        # Получаем блюда, добавленные пользователем
        user_dishes = models.UserDish.objects.filter(user=request.user)  
        added_dishes = [user_dish.dish for user_dish in user_dishes]
        
        # Получаем созданные блюда для текущего пользователя
        created_dishes = models.UserCreatedDish.objects.filter(user=request.user)

        # Объединяем блюда и помечаем их тип
        for dish in added_dishes:
            dish.ingredients_list = ', '.join([
                f"{ingredient.product.name}: {ingredient.weight} гр." 
                for ingredient in dish.ingredients.all()
            ])
        
        for created_dish in created_dishes:
            created_dish.ingredients_list = ', '.join([
                f"{user_created_dish_product.product.name}: {user_created_dish_product.weight} гр." 
                for user_created_dish_product in models.UserCreatedDishProduct.objects.filter(dish=created_dish)
            ])

        dishes = list(added_dishes) + list(created_dishes)
        for dish in dishes:
            dish.type = 'created' if isinstance(dish, models.UserCreatedDish) else 'added'

        return render(request, self.template_name, {
            'dishes': dishes,
        })
        
class UserCreateDishView(View):
    def get(self, request):
        products = models.Product.objects.all()
        categories = models.Dish.objects.exclude(categorys='').values_list('categorys', flat=True).distinct()
        return render(request, 'dishes/user_create_dish.html', {
            'products': products,
            'categories': categories,
        })

    def post(self, request):
        products = models.Product.objects.all()
        categories = models.Dish.objects.exclude(categorys='').values_list('categorys', flat=True).distinct()
        
        # Получаем данные из формы
        name = request.POST.get('name')
        images = request.FILES.get('images')
        category = request.POST.get('category')
        recipes = request.POST.get('recipes')

        if all([name, recipes]):
            existing_dish = models.UserCreatedDish.objects.filter(name=name, user=request.user).first()
            if existing_dish:
                error_message = "Такое блюдо уже создано."
                return render(request, 'dishes/user_create_dish.html', {
                    'error': error_message,
                    'products': products,
                    'categories': categories,
                })

            # Создаем новое блюдо и сохраняем его в базе данных
            new_dish = models.UserCreatedDish(
                user=request.user,
                name=name,
                images=images,
                category=category,
                recipes=recipes,
            )

            try:
                new_dish.save()
                # Получаем ингредиенты
                product_ids = request.POST.getlist('products')
                weights = request.POST.getlist('weights')

                # Создание взаимосвязей
                for product_id, weight in zip(product_ids, weights):
                    if weight and weight.isdigit():
                        user_created_dish_product = models.UserCreatedDishProduct(
                            dish=new_dish,
                            product_id=product_id,
                            weight=float(weight)
                        )
                        user_created_dish_product.save()

                return redirect('dishes:saved_dishes')

            except Exception as e:
                print("Ошибка при сохранении блюда:", e)
                return render(request, 'dishes/user_create_dish.html', {
                    'error': "Произошла ошибка при сохранении.",
                    'products': products,
                    'categories': categories,
                })

        return render(request, 'dishes/user_create_dish.html', {
            'error': "Заполните все обязательные поля.",
            'products': products,
            'categories': categories,
        })

class DeleteDishView(View):
    def post(self, request, dish_id, dish_type):
        if dish_type == "user":
            try:
                user_dish = models.UserDish.objects.get(dish_id=dish_id, user=request.user)
                user_dish.delete()
                messages.success(request, 'Блюдо успешно удалено.')
            except models.UserDish.DoesNotExist:
                messages.error(request, 'Блюдо не найдено.')
            except Exception as e:
                print(f"Ошибка при удалении блюда: {e}")
                messages.error(request, 'Произошла ошибка на сервере.')
            return redirect('profile')

        elif dish_type == "created":
            dish = get_object_or_404(models.UserCreatedDish, id=dish_id)

            if dish.user == request.user:
                dish.delete()
                messages.success(request, 'Блюдо успешно удалено.')
            else:
                messages.error(request, 'Вы не имеете права удалять это блюдо.')

            return redirect('dishes:saved_dishes')

        return redirect('dishes:saved_dishes')