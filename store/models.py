from django.db import models

# Create your models here.

class Product(models.Model):
    description = models.CharField(max_length=600)
    title = models.CharField(max_length=600)
    price = models.IntegerField()
    daysBeforeShipping = models.IntegerField()
    img = models.ImageField()
    pid = id

    # create staticfiles and look up db storage (check credentials, look for similar errors) figure out pid
