# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2020-04-27 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shaw_queue', '0044_auto_20200426_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='customer_title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
