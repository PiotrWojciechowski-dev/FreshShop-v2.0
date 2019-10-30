from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
# Create your views here.

def home_view(request):
    template_name = 'home.html'
    return render(request, 'home.html', {})

def product_view(request):
    template_name = 'products.html'
    return render(request, 'products.html', {})
