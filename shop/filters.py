import django_filters
from django import forms
from .models import Product, Category 
    
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name='price')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'price__gt', 'price__lt', 'available']
