from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
import sys

sys.path.append('../')

from store.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    def add(self, pid):
        product = Product.objects.get(id=pid)
        try:
            existing_order = ProductOrder.objects.get(product=product, cart=self)
            existing_order.quantity += 1
            existing_order.save()
        except ProductOrder.DoesNotExist:
            order = ProductOrder.objects.create(
                product=product,
                cart=self,
                quantity=1
            )
            order.save()

    def remove(self, pid):
        product = Product.objects.get(id=pid)
        try:
            existing_order = ProductOrder.objects.get(product=product, cart=self)
            existing_order.delete()
        except:
            pass

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
