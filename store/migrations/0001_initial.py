# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-18 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=600)),
                ('title', models.CharField(max_length=600)),
                ('price', models.IntegerField()),
                ('daysBeforeShipping', models.IntegerField()),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
    ]