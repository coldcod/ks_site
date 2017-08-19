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
    img = models.ImageField()
    pubdate = models.DateTimeField(default=datetime.now())
    stock = models.IntegerField(default=2)
    pid = models.SlugField(default=slugify(" "))
    def save(self, *args, **kwargs):
        def_slug = AutoSlugField(('def_slug'), max_length=10, unique=True, populate_from=('title'))
        self.pid = slugify(def_slug)
        super(Product, self).save(*args, **kwargs)

'''@receiver(models.signals.post_save, sender=Product, dispatch_uid="generate_pid")
def gen_pid(sender, **kwargs):
    if kwargs.get('created', False):
        instance = kwargs.get('instance')
        instance.pid = instance.title.replace(" ", "-") + instance.id()
        instance.save()'''

    # create staticfiles and look up db storage (check credentials, look for similar errors) figure out pid
