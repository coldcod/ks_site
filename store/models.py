from django.db import models
from django.dispatch import receiver
from datetime import datetime
from django.template.defaultfilters import slugify
from django_extensions.db.fields import AutoSlugField

# Create your models here.

class Product(models.Model):
    description = models.CharField(max_length=600)
    title = models.CharField(max_length=600)
    price = models.IntegerField()
    daysBeforeShipping = models.CharField(max_length=10)
    img = models.ImageField(null=True, blank=True)
    pubdate = models.DateTimeField(default=datetime.now())
    stock = models.IntegerField(default=2)
    pid = models.SlugField(default=slugify(" "), null=True, blank=True)
    def save(self, *args, **kwargs):
        slug_def = self.title + "-" + str(self.id)
        self.pid = slugify(slug_def.lower())
        super(Product, self).save(*args, **kwargs)

    # create staticfiles and look up db storage (check credentials, look for similar errors) figure out pid
