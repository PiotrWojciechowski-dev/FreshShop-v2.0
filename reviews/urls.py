from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.review_list, name='review_list')
]