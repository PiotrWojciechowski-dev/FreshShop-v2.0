# Generated by Django 2.2.5 on 2019-11-27 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20191127_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='county',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
