from django import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view(), name ='signup'),
]