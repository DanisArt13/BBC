# Generated by Django 5.0.7 on 2024-10-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rating_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='total_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.IntegerField(),
        ),
    ]
