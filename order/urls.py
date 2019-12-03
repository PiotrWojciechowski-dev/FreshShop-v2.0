from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created, name='order_created'),
    path('payment', views.payment_method, name='payment'),
    path('history/', views.order_history, name='order_history'),
    path('cancel/<int:order_id>', views.cancel_order, name='cancel_order'),
]