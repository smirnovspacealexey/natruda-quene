# Generated by Django 3.2.4 on 2022-06-27 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0054_auto_20210626_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='fired',
            field=models.BooleanField(default='False'),
        ),
    ]
