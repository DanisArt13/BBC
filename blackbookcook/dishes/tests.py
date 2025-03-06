from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Dish, UserDish

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
            return HttpResponseRedirect(reverse('dishes'))

        # Перенаправляем на ту же страницу с блюдами
        return HttpResponseRedirect(reverse('dishes'))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dishes'))
