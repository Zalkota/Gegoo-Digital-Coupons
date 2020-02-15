from django import forms

class ApplyCouponForm(forms.Form):
    code = forms.CharField(label='Code', max_length=50)