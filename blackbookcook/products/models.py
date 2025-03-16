from django.db import models
from django.db.models import SmallAutoField, DecimalField, CharField, ImageField, TextField, ForeignKey, ManyToManyField

# Модель Product
class Product(models.Model):
    id = SmallAutoField(primary_key=True)
    name = CharField(max_length=50)
    calories = TextField()
    fats = TextField()
    proteins = TextField()
    carbohydrates = TextField()
    water = TextField()
    sugar = TextField()
    image_url = models.CharField(max_length=255, null=True)
    categories = CharField(max_length=50, null=True)
    text = TextField(null=True)
    area = CharField(max_length=50, null=True)

    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return f'{self.id}\n{self.name}\n{self.calories}\n{self.categories}\n{self.image_url}'

