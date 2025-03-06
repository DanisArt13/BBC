""" Блюда """

from django.urls import path
from dishes import views

app_name = 'dishes'

urlpatterns = [
    path('', views.DishView.as_view(), name='dishes'),  # URL для входа
    path('add_user_dish/', views.AddUserDishView.as_view(), name='add_user_dish'),
    path('saved_dishes/', views.SavedDishesView.as_view(), name='saved_dishes'),
    path('delete_dish/<int:dish_id>/<str:dish_type>/', views.DeleteDishView.as_view(), name='delete_dish'),
    path('user-create-dish/', views.UserCreateDishView.as_view(), name='user_create_dish'),
]