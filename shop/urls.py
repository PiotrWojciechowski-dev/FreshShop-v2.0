from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('grooming_tips/', views.grooming_tips_view, name='grooming_tips'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
    path('products/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
<<<<<<< HEAD
=======
    
>>>>>>> master
]