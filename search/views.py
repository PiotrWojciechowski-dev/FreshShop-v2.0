from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
from shop.filters import ProductFilter
# Create your views here.

def search_result(request):
    products = None
    query = None
    products_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    products = products_filter.qs
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
    return render(request, 'search.html', {'query':query, 'products':products, 'filter': products_filter,})
