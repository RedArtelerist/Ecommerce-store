from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)