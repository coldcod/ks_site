# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-20 07:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20170820_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 20, 7, 48, 25, 679472, tzinfo=utc)),
        ),
    ]
