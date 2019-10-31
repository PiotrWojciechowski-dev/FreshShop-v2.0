from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_view, name='products'),
    path('faq/', views.faq_view, name='faq'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
]