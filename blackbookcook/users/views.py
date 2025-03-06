from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.core.files.storage import default_storage
import os
from . import models, forms

# Create your views here.
User = get_user_model()

class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        form = forms.UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Проверка пользователя в базе данных db_users
            user = authenticate(username=username, password=password)
            if user:
                print("Authenticated user:", user.username)
                login(request, user)
                return redirect('home:home')  # Перенаправляем на главную страницу после входа
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
                print("Authentication failed for user:", username)
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    def get(self, request):
        form = forms.UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  
            user.save()  
            user.create_profile()
             
            username = form.cleaned_data.get('username')
            messages.success(request, f'Учетная запись {username} создана! Теперь вы можете войти.')
            return redirect('users:login')  
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        
        return render(request, 'users/register.html', {'form': form})

class LogoutView(DjangoLogoutView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)  
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect(reverse('users:login')) 
        
class ProfileView(View):
    def get(self, request):
        user_profile = models.UserProfile.objects.get(user=request.user)
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=user_profile)
        return render(request, 'users/profile.html', {
            'user_profile': user_profile,
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_profile = models.UserProfile.objects.get(user=request.user)
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('/user/profile/')

        return render(request, 'users/profile.html', {
            'user_profile': user_profile,
            'user_form': user_form,
            'profile_form': profile_form
        })