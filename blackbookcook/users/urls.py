from django.urls import path
from users import views
from .views import LoginView, RegisterView, ProfileView, LogoutView, ProfileView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # URL для входа
    path('register/', RegisterView.as_view(), name='register'),  # URL для регистрации
    path('profile/', ProfileView.as_view(), name='profile'),  # URL для профиля
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),  # URL для выхода
]

