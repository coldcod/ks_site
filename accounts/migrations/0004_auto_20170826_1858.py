# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-26 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170826_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='cc',
            field=models.CharField(default='', max_length=200),
        ),
    ]