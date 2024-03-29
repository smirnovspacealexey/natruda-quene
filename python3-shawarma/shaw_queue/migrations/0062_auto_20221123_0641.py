# Generated by Django 3.2.4 on 2022-11-23 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0061_cookingtime_default'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productvariant',
            options={'ordering': ('title', 'customer_title')},
        ),
        migrations.AlterField(
            model_name='cookingtime',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='shaw_queue.MenuCategory', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='cookingtime',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='shaw_queue.Menu', verbose_name='Товары'),
        ),
    ]
