# Generated by Django 3.2.4 on 2023-03-18 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_auto_20230318_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangosettings',
            name='from_extension',
            field=models.CharField(default=1, max_length=10, verbose_name='Идентификатор сотрудника'),
            preserve_default=False,
        ),
    ]
