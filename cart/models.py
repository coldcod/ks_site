from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
import sys
sys.path.append('../')
from store.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    session_id = models.CharField(default='', max_length=500)
    order_date = models.DateTimeField(default=timezone.now)
    def _add(self, pid):
        product = Product.objects.get(pid=pid)
        order, created = ProductOrder.objects.get_or_create(product=product, cart=self)
        order.quantity += 1
        order.save()

    def _remove(self, pid):
        product = Product.objects.get(pid=pid)
        try:
            existing_order = ProductOrder.objects.get(product=product, cart=self)
            existing_order.delete()
        except:
            pass

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.product.title
