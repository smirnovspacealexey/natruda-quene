# Generated by Django 3.2.4 on 2023-10-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0076_order_paid_with_sms'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='burger_completed',
            field=models.BooleanField(default=False, verbose_name='Burger Completed'),
        ),
        migrations.AddField(
            model_name='order',
            name='coffee_completed',
            field=models.BooleanField(default=False, verbose_name='Coffee Completed'),
        ),
        migrations.AddField(
            model_name='order',
            name='with_burger',
            field=models.BooleanField(default=False, verbose_name='With Burger'),
        ),
        migrations.AddField(
            model_name='order',
            name='with_coffee',
            field=models.BooleanField(default=False, verbose_name='With Coffee'),
        ),
    ]
