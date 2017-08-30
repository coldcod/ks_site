# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-30 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_id',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
