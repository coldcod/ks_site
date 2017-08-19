from django.db import models
from django.dispatch import receiver
from datetime import datetime
import django

# Create your models here.

class Product(models.Model):

    def gen_pid(self):
        return self.title.replace(" ", "-") + str(self.id)

    description = models.CharField(max_length=600)
    title = models.CharField(max_length=600)
    price = models.IntegerField()
    daysBeforeShipping = models.IntegerField()
    img = models.ImageField()
    pubdate = models.DateTimeField(default=django.utils.timezone.now)
    stock = models.IntegerField()

    def __str__(self):
        return str(self.title) + " | Rs. " + str(self.price)
    '''def __init__(self, *args, **kwargs):
        self.pid = self.title.replace(" ", "-") + str(self.id)
        super(Product, self).__init__(*args, **kwargs)'''

    # create staticfiles and look up db storage (check credentials, look for similar errors) figure out pid

@receiver(models.signals.post_save, sender=Product, dispatch_uid="generate_pid")
def generate_pid(sender, **kwargs):
    if kwargs.get('created', False):
        instance = kwargs.get('instance')
        instance.pid = instance.title.replace(" ", "-") + str(instance.id)
        instance.save()
