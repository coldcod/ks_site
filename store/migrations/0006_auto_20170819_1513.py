# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-19 09:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20170819_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pubdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
