from django.db import models
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
from django.template.defaultfilters import slugify

from .pid import pid

# Create your models here.

class Product(models.Model):
    description = models.CharField(max_length=600)
    title = models.CharField(max_length=600)
    og_price = models.IntegerField(default=0)
    price = models.IntegerField()
    daysBeforeShipping = models.CharField(max_length=10)
    img = models.ImageField(null=True, blank=True)
    pubdate = models.DateTimeField(default=timezone.now)
    stock = models.IntegerField(default=2)
    category = models.CharField(max_length=200)
    discount_in_percent = models.IntegerField(default=0)
    pid = models.SlugField(default=slugify(" "), null=True, blank=True, unique=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        hash_pid = pid.make_token(self)
        self.pid = hash_pid
        self.title = self.title.title()
        self.category = self.category.title()
        self.og_price = self.price
        self.price -= (self.discount_in_percent / 100.0) * self.price
        super(Product, self).save(*args, **kwargs)

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="images")
    image = models.ImageField()
    def __str__(self):
        return str(self.image)
