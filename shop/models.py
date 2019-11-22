from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField 
from imagekit.processors import ResizeToFill

# Create your models here.

class Category(models.Model):
    name = models.TextField()

    def get_product(self):
        return Product.objects.filter(category=self)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.id])

class Product(models.Model):
    name = models.TextField()
    category = models.ForeignKey(Category, related_name= 'products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(90,90)], format='JPEG', options={'quality': 60})
    description = models.TextField()
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name  