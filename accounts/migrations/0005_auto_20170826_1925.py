# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 13:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170826_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
