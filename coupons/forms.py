from django import forms
from django.forms import TextInput


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your coupon code',
        'aria-label': 'Coupon code'
    }), label='')