from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.TextField()

    def get_product(self):
        return Product.objects.filter(category=self)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)