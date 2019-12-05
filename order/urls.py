from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('history/', views.order_history, name='order_history'),
    path('cancel/<int:order_id>', views.cancel_order, name='cancel_order'),
    path('created/<int:order_id>', views.order_created, name='order_created'),
    path('payment/<int:order_id>', views.payment_method, name='payment'),
    path('cancelled/', views.payment_cancelled, name='cancelled'),
    path('payment_made/<int:order_id>', views.payment_made, name='payment_made'),
    path('payment_made_paypal', views.payment_made_paypal, name='payment_made_paypal')
]