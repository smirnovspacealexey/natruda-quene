# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2021-04-03 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0051_macroproductcontent_menu_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='macroproduct',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='img/icons', verbose_name='Иконка'),
        ),
    ]
