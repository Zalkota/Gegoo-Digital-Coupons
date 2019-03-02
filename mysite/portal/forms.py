from django import forms
from .models import Review
#from django.forms import ModelForm
#from .models import Contact

#class ContactForm(ModelForm):
#    class Meta:
#        model = Contact
#        fields = '__all__'

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')
        widgets = {'review_user': forms.HiddenInput(), 'review_course': forms.HiddenInput(), 'summary':  forms.Textarea}


#class ProductForm(ModelForm):
#    class Meta:
#        model = Product
#        fields = '__all__'
