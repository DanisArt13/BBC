# Generated by Django 5.0.7 on 2024-10-11 22:05

import dishes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0005_usercreateddish_usercreateddishproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercreateddish',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to=dishes.models.user_dish_image_path),
        ),
    ]
