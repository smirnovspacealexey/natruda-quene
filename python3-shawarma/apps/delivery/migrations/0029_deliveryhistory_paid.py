# Generated by Django 3.2.4 on 2023-06-16 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0028_auto_20230616_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryhistory',
            name='paid',
            field=models.BooleanField(default=False, help_text='заявка оплачена'),
        ),
    ]
