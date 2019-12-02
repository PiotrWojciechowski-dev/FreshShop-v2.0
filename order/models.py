from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from vouchers.models import Voucher
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Order(models.Model):
    first_name = models.CharField(
        max_length=250,
        null=True,
    )

    last_name = models.CharField(
        max_length=250,
        null=True,
    )

    emailAddress = models.EmailField(
        max_length=250,
        blank=True,
    )

    addressline1 = models.CharField(
        max_length=250,
        null=True,
        help_text='Street address, P.O box, company name, c/o'
    )

    addressline2 = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text='Appartment, suite, unit. building, floor, etc.'
    )

    code = models.CharField(
        max_length=10,
        null=True,
        blank=False,
    )

    city = models.CharField(
        max_length=250,
        null=True,
    )

    county = models.CharField(
        max_length=250,
        null=True,
    )
    
    country = CountryField(null=True).formfield()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = 'Order'
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_items(self):
        return OrderItem.objects.filter(order=self)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity  