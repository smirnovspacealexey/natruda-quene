# Generated by Django 3.2.4 on 2022-12-12 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0065_order_is_pickup'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookingTimerOrderContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True, verbose_name='время начала готовки')),
                ('order_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shaw_queue.ordercontent')),
            ],
        ),
    ]
