from django.db import models
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
from django.template.defaultfilters import slugify
from subprocess import call
from django.contrib.auth.models import User

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
    notes = models.CharField(max_length=60, blank=True, null=True, default=None)
    pid = models.SlugField(default=slugify(" "), null=True, blank=True, unique=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
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
        call(['python3', 'manage.py', 'collectstatic', '--noinput'])
        super(Product, self).save(*args, **kwargs)

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="images")
    image = models.ImageField()
    def __str__(self):
        return str(self.image)
    def save(self, *args, **kwargs):
        call(['python3', 'manage.py', 'collectstatic', '--noinput'])
        super(ProductImages, self).save(*args, **kwargs)
