# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-20 06:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20170819_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.SlugField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 20, 12, 10, 40, 936619)),
        ),
    ]
