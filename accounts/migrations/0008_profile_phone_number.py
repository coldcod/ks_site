# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-01 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]