# Generated by Django 3.2.4 on 2023-11-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0082_auto_20231110_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='macroproduct',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='скрыть'),
        ),
    ]
