from django.db import models
from django.db.models import CASCADE


class Item(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username


class Deal(models.Model):
    item = models.ForeignKey(Item, CASCADE, 'deals')
    total = models.PositiveIntegerField()
    customer = models.ForeignKey(Customer, CASCADE, 'deals')
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(blank=False)
