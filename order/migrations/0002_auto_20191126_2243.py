# Generated by Django 2.2.5 on 2019-11-26 22:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('vouchers', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'Shipping Address', 'verbose_name_plural': 'Shipping Addresses'},
        ),
        migrations.AddField(
            model_name='order',
            name='address1',
            field=models.CharField(max_length=250, null=True, verbose_name='Address line 1'),
        ),
        migrations.AddField(
            model_name='order',
            name='address2',
            field=models.CharField(max_length=250, null=True, verbose_name='Address line 2'),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=250, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=10, null=True, verbose_name='ZIP / Postal code'),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=250, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=250, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='order',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order', to='vouchers.Voucher'),
        ),
        migrations.AlterField(
            model_name='order',
            name='emailAddress',
            field=models.EmailField(blank=True, max_length=250, verbose_name='Email Address'),
        ),
        migrations.AlterModelTable(
            name='order',
            table='ShippingAddress',
        ),
    ]
