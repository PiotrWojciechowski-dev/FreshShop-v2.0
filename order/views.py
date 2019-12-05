from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import IEPostalAddressForm
from cart.models import Cart, CartItem
from cart.cart import Cart
from shop.models import Product
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.conf import settings
import stripe
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from .email import Email
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = IEPostalAddressForm(request.POST)
        if form.is_valid():
            print("Inside if")
            order = form.save(commit=False)
            if cart.voucher:
                order.voucher = cart.voucher
                order.discount = cart.voucher.discount
            order = form.save()
            order.save()
         
        for order_item in cart:
            OrderItem.objects.create(order=order,
                                    product=order_item['product'],
                                    price=order_item['price'],
                                    quantity=order_item['quantity'])
        cart.clear()
        total = Cart.get_total_price_after_discount(cart)
        Email.sendOrderConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
        return render(request, 'order_created.html', {'order': order, 'total':total})
    else: 
        print('Inside else')
        form = IEPostalAddressForm()
    return render(request, 'order.html',{'cart':cart, 'form':form})

def order_created(request):
    order = get_object_or_404(Order, id=order_id)
    total = order.get_total()
    order.paid = True
    order.save()
    Email.sendOrderConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
    return render(request, 'order_created.html', {'order':order})

@login_required()
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(emailAddress=email)
        '''Pagination code'''
        paginator = Paginator(order_details, 3)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:    
            orders = paginator.get_page(page)
        except (EmptyPage, InvalidPage):
            orders = paginator.page(paginator.num_pages)
        context = {
            'orders': orders,
        }
    return render(request, 'order_list.html', context)

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created
    current_date = datetime.now(timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60.0
    if minutes_diff <= 500:
        order.delete()
        adjust_stock(request, order_id)
        messages.add_message(request, messages.INFO, 
                    'Order is now cancelled')
    else:
        messages.add_message(request, messages.INFO,
                    'Sorry, it is too late to cancel this order')
    Email.sendCancelationConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country)
    return redirect('order_history')



def adjust_stock(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        product = get_object_or_404(Product, name=order_item.product)
        product.stock += order_item.quantity
        product.save()  


def payment_method(request, order_id):
    print(order_id)
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    total = order.get_total_cost()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = "Online Shop"
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://127.0.0.1:8000/order/payment_made/{}'.format(order.id),
        'cancel_return': 'http://{}{}'.format(host, reverse('cancelled')),  
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    
    return render(request, 'payment.html', {'form':form, 'order':order, 'data_key':data_key, 'stripe_total':stripe_total, 'description':description})

@csrf_exempt
def payment_made(request, order_id):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=str(int(total * 100)),
            currency='EUR',
            description='Credit card charge',
            source=request.POST['stripetoken']
        )
    order = get_object_or_404(Order, id=order_id)
    total = order.get_total()
    order.paid = True
    order.save()
    Email.sendPaymentConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
    return render(request, 'payment_made.html', {'order':order})

@csrf_exempt
def payment_made_paypal(request):
    order = get_object_or_404(Order, id=order_id)
    total = order.get_total()
    order.paid = True
    order.save()
    Email.sendPaymentConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
    return render(request, 'payment_made_paypal.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'cancelled.html')