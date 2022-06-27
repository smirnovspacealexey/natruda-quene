# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2021-03-14 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('shaw_queue', '0049_auto_20200720_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='MacroProductContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                (
                    'customer_title',
                    models.CharField(default='', max_length=200, verbose_name='Название для покупателя')),
                ('picture',
                 models.ImageField(blank=True, null=True, upload_to='img/category_pictures', verbose_name='Иконка')),
                ('customer_appropriate',
                 models.BooleanField(default=False, verbose_name='Подходит для демонстрации покупателю')),
                ('content_option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                     to='shaw_queue.ContentOption',
                                                     verbose_name='Вариант содержимого')),
                ('macro_product',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shaw_queue.MacroProduct',
                                   verbose_name='Макротовар')),
            ],
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='content_option',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='macro_product',
        ),
        migrations.AlterField(
            model_name='ordercontentoption',
            name='content_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_item',
                                    to='shaw_queue.OrderContent', verbose_name='Товар из заказа'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='macro_product_content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='shaw_queue.MacroProductContent', verbose_name='Содержимое макротовара'),
        ),
    ]
