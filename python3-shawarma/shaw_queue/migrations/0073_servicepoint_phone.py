# Generated by Django 3.2.4 on 2023-04-05 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0072_auto_20230405_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepoint',
            name='phone',
            field=models.CharField(default='', help_text='Для доставки', max_length=200),
        ),
    ]
