from django import forms
from orders.models import Order
from orders.utils import queryset_cities


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_first_name', 'customer_last_name', 'customer_email', 'customer_phone',
                  'city', 'address', 'delivery', 'paymentMethod',
                  'recipient_first_name', 'recipient_last_name', 'recipient_email']
        widgets = {
            'customer_first_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'first name'}),
            'customer_last_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'last name'}),
            'customer_email': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'email'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'mobile phone'}),
            'city': forms.Select(choices=queryset_cities(), attrs={'class': 'form-control', 'data-name': 'city'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'address'}),
            'recipient_first_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'first name'}),
            'recipient_last_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'last name'}),
            'recipient_email': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'email'}),
            'delivery': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'paymentMethod': forms.RadioSelect(attrs={'class': 'custom-control-input'})
        }