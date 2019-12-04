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
            order = form.save()
            order.save()
         
        for order_item in cart:
            OrderItem.objects.create(order=order,
                                    product=order_item['product'],
                                    price=order_item['price'],
                                    quantity=order_item['quantity'])
        cart.clear()
        #request.session['order_id'] = order.id
        # set up stripe
        total = Cart.get_total_price_after_discount(cart)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_total = int(total * 100)
        description = "Online Shop"
        data_key = settings.STRIPE_PUBLISHABLE_KEY
        Email.sendOrderConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
        return render(request, 'payment.html', {'order': order, 'data_key':data_key, 'stripe_total':stripe_total, 'description':description, 'total':total})

        '''
        cart.clear()
        order_created.delay(order.id)
        request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))
        
        Reduce Stock when order is placed or saved
        products = Product.objects.get(id=order_item.product.id)
        if products.stock > 0:
            products.stock = int(order_item.product.stock - order_item.quantity)
        products.save()
        order_item.delete()
        '''
    else: 
        print('Inside else')
        form = IEPostalAddressForm()
         # set up stripe
        total = Cart.get_total_price_after_discount(cart)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_total = int(total * 100)
        description = "Online Shop"
        data_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'order.html',{'cart':cart,
                                        'form':form, 'data_key':data_key, 'stripe_total':stripe_total, 'description':description, 'total':total})
    '''
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.create(emailAddress = email)
        order_details.save()
    try:
        for order_item in cart_items:
            oi = OrderItem.objects.create(
                product = order_item.product.name,
                quantity = order_item.quantity,
                price = order_item.product.price,
                order = order_details
            )
            oi.save()

            Reduce Stock when order is placed or saved
            products = Product.objects.get(id=order_item.product.id)
            if products.stock > 0:
                products.stock = int(order_item.product.stock - order_item.quantity)
            products.save()
            order_item.delete()
    except ObjectDoesNotExist:
        pass
   
    return render(request, 'order.html', {'cart_items':cart_items, 'total':total})
'''

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
    Email.sendOrderConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
    return redirect('order_history')



def adjust_stock(request):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        product = get_object_or_404(Product, name=order_item.product)
        product.stock += order_item.quantity
        product.save()  


def payment_method(request, total=0):
    order = get_object_or_404(Order, id=order_id)
    #order - get_object_or_404(Order, id-order_id)
    #host = request.get_host()
    #order = get_object_or_404(Order, id=order_id)
    total = order.get_total_cost()
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=str(int(total * 100)),
            currency='EUR',
            description='Credit card charge',
            source=request.POST['stripetoken']
        )
    """
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('order_created')),
        'cancel_return': 'http://{}{}'.format(host, reverse('cancelled')),  
    }
    form = PaypalPaymentsForm(initial=paypal_dict)
    """
    
    return render(request, 'payment.html', {'form':form, 'order':order})

@csrf_exempt
def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total = order.get_total()
    order.paid = True
    order.save()
    Email.sendPaymentConfirmation(request, order.emailAddress, order.id, order.addressline1, order.addressline2, order.code, order.city, order.county, order.country, total)
    return render(request, 'order_created.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'cancelled.html')