# Generated by Django 2.2.5 on 2019-12-04 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]
