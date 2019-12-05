from django import forms
from .models import Order
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

class IEPostalAddressForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'emailAddress', 'addressline1', 'addressline2', 'code', 'city', 'county', 'country']

class LoggedInIEPostalAddressForm(forms.ModelForm):
    country = CountryField().formfield()
    class Meta:
        model = Order
        fields = ['addressline1', 'addressline2', 'code', 'city', 'county', 'country']
