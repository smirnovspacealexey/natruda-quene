# Generated by Django 3.2.4 on 2023-02-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0069_menu_qr_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercontent',
            name='qr',
            field=models.TextField(blank=True, null=True),
        ),
    ]
