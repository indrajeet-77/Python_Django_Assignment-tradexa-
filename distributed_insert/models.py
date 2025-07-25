from django.db import models

# My models
from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()

    class Meta:
        app_label = 'distributed_insert'

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()

    class Meta:
        app_label = 'distributed_insert'

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        app_label = 'distributed_insert'
