from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage
# Create your views here.

def home_view(request):
    template_name = 'home.html'
    return render(request, 'home.html', {})

def grooming_tips_view(request):
    template_name = 'grooming_tips.html'
    return render(request, 'grooming_tips.html', {})

def contact_us_view(request):
    template_name = 'contact_us.html'
    return render(request, 'contact_us.html', {})

def product_list(request, category_id=None):
    category = None
    product_list = Product.objects.all()
    ccat = Category.objects.annotate(num_products=Count('products'))
    if(category_id):
        category = get_object_or_404(Category, id=category_id)
        product_list = product_list.filter(category=category)
    '''Pagination code'''
    paginator = Paginator(product_list, 3)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:    
        products = paginator.get_page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    context = {
            'products': products,
            'countcat': ccat,
        }
    return render(request, 'products.html', context)