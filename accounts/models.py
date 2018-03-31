# 'Accounts' apps models.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    alt_phone_number = models.CharField(max_length=14)
    address = models.CharField(max_length=600, default="Jalandhar")
    email_confirmed = models.BooleanField(default=False)
    shopname = models.CharField(max_length=100)
    gst = models.CharField(max_length=200)
    pan = models.CharField(max_length=200)
    prodtype = models.CharField(max_length=200)
    accountholder = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    IFSC_code = models.CharField(max_length=200)
    def __str__(self):
        return str(self.name) + " - " + str(self.shopname)

@receiver(post_save, sender=User)
def add_profile_info(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
