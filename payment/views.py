from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def payment_method(request, total=0):
    order_id = request.session.get('order_id')
    order - get_object_or_404(Order, id-order_id)
    host = request.get_host()
    total = order_create.total
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=str(int(total * 100)),
            currency='EUR',
            description='Credit card charge',
            source=request.POST['stripetoken']
        )
    
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),  
    }
    form = PaypalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment.html', {'order':order, 'form':form})

@csrf_exempt
def order_created(request):
    return render(request, 'order_created.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'cancelled.html')