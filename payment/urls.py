from django.urls import path
from . import views

urlpatterns = [
    path('created/', views.order_created, name='order_created'),
    path('payment', views.payment_method, name='payment'),
    path('cancelled', views.payment_cancelled, name='cancelled'),
]