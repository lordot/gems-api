from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     pass
#
#
# class Gem(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50, unique=True, blank=False)
#
#     def __str__(self):
#         return self.name


class Deal(models.Model):
    item = models.CharField(max_length=15)
    total = models.PositiveIntegerField()
    customer = models.CharField(max_length=15)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(blank=False)

