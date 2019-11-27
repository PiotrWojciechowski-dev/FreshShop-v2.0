<<<<<<< HEAD
from django import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view(), name ='signup'),
=======
from django.urls import path
from . import views

urlpatterns = [
    path('email/', views.index, name='index'),
>>>>>>> 93ea683fd34a158c593e981195b159bb7b528756
]