# Generated by Django 5.0.7 on 2024-10-04 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0003_dish_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='dishes/images'),
        ),
    ]
