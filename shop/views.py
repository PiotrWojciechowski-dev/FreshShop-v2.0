from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from cart.forms import CartAddProductForm

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


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    product_list = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product_list = products.filter(category=category)
    '''Pagination code'''
    paginator = Paginator(product_list, 6)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:    
        products = paginator.get_page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
    return render(request, 'product/products.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'product/product_detail.html',
                  {'product': product,
                  'cart_product_form': cart_product_form})   