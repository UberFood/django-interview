from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    price = models.IntegerField(default=1)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
