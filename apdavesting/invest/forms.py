from django import forms
from .models import buyRequest, sellRequest

class BuyRequestForm(forms.ModelForm):
    class Meta:
        model = buyRequest
        fields = ['ticker', 'shares']

class SellRequestForm(forms.ModelForm):
    class Meta:
        model = sellRequest
        fields = ['position', 'shares']

        