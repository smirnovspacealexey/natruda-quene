# Generated by Django 3.2.4 on 2023-04-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_auto_20230403_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryhistory',
            name='six_numbers',
            field=models.CharField(default='834995', max_length=200, verbose_name='код для курьера'),
        ),
        migrations.AlterField(
            model_name='deliveryhistory',
            name='uuid',
            field=models.CharField(default='e611fe57-fbd8-4cd9-9b04-5c4958d74ebf', max_length=200),
        ),
    ]
