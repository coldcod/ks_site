# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-20 07:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20170820_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pubdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
