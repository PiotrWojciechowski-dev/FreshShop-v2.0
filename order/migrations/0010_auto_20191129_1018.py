# Generated by Django 2.2.5 on 2019-11-29 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_county'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='voucher',
        ),
    ]
