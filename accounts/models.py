# 'Accounts' apps models.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=600)
    cc = models.CharField(max_length=200, default='')
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.address) + ' - ' + str(self.cc)

@receiver(post_save, sender=User)
def add_profile_info(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
