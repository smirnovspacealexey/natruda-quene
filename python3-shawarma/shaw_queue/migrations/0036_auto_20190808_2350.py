# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-08-08 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0035_auto_20190731_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Is canceled'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='Is dinished'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='daily_number',
            field=models.IntegerField(verbose_name='номер за день'),
        ),
    ]
