# Generated by Django 5.0.7 on 2024-09-19 13:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0002_userdish'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
