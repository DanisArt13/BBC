from django.db import models
from django.db.models import SmallAutoField, DecimalField, CharField, ImageField, TextField, ForeignKey, ManyToManyField

# Модель Product
class Product(models.Model):
    id = SmallAutoField(primary_key=True)
    name = CharField(max_length=50)
    images = models.CharField(max_length=255, null=True)
    text = TextField(null=True)
    proteins = DecimalField(max_digits=5, decimal_places=2)
    fats = DecimalField(max_digits=5, decimal_places=2)
    carbs = DecimalField(max_digits=5, decimal_places=2)
    kcals = DecimalField(max_digits=5, decimal_places=2)
    categorys = CharField(max_length=50, null=True)
    areas = CharField(max_length=50, null=True)

    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return f'{self.id}\n{self.name}\n{self.kcals}\n{self.proteins}\n{self.fats}\n{self.carbs}'

