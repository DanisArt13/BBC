from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def user_profile_image_path(instance, filename):
    return f'users/{instance.user.id}/profile_image/{filename}'

class User(AbstractUser):
    
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username    
        
    def create_profile(self):
        if not hasattr(self, 'userprofile'):
            UserProfile.objects.create(user=self)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)  
    middle_name = models.CharField(max_length=30, null=True, blank=True) 
    profile_image = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True, verbose_name="Аватар")
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"{self.user.username}'s Profile"
        
