# Generated by Django 2.2.5 on 2019-12-05 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_review_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
