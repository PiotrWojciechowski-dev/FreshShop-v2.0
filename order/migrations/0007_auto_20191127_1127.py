# Generated by Django 2.2.5 on 2019-11-27 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False


    dependencies = [
        ('order', '0006_auto_20191127_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.AlterField(
            model_name='order',
            name='addressline1',
            field=models.CharField(help_text='Street address, P.O box, company name, c/o', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='addressline2',
            field=models.CharField(help_text='Appartment, suite, unit. building, floor, etc.', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='vouchers.Voucher'),
        ),
    ]
