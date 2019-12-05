import django_filters
from .models import Product, Category 
    
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    created = django_filters.NumberFilter(field_name='created', lookup_expr='year')
    created__gt = django_filters.NumberFilter(field_name='created', lookup_expr='year__gt')
    created__lt = django_filters.NumberFilter(field_name='created', lookup_expr='year__lt')

    category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category','price', 'created', 'name', 'available']