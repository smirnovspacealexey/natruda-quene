# Generated by Django 3.2.4 on 2023-04-13 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0011_yandexsettings_geocoder_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('km', models.IntegerField(default=0, verbose_name='км')),
                ('roubles', models.IntegerField(default=0, verbose_name='цена')),
            ],
        ),
        migrations.CreateModel(
            name='DeliverySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distances', models.ManyToManyField(blank=True, to='delivery.DeliveryDistance', verbose_name='дистанции')),
            ],
        ),
    ]
