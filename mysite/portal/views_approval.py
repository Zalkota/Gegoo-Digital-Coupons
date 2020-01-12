# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from portal import models as portal_models
from .forms import MerchantApprovalForm
from django.views.generic.edit import FormView, FormMixin
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from location.functions import set_location_cookies, get_ip, get_or_set_location
from users.decorators import user_is_merchant



class MerchantApprovalFormView(FormView):
    form_class = MerchantApprovalForm
    success_url = reverse_lazy('merchant-approval-landing-page')
    template_name = 'portal/approval/merchant_approval_form.html'


    def form_valid(self, form):
        ContactForm = form.save(commit=False)
        ContactForm.name = form.cleaned_data['name']
        ContactForm.email = form.cleaned_data['email']
        ContactForm.phone = form.cleaned_data['phone']
        ContactForm.description = form.cleaned_data['description']
        ContactForm.save()
        #send_email(ContactForm.name, ContactForm.email, ContactForm.phone, ContactForm.description)

        #template = get_template('contact_template.txt')
        #context = Context({
        #    'contact_name': contact_name,
        #    'contact_email': contact_email,
        #    'form_content': form_content
        #})
        #content = template.render(context)

        #email = EmailMessage(
        #    'New contact form submission',
        #    content,
        #    'Your website ' + '',
        #    ['youremail@gmail.com'],
        #    headers = {'Reply-To': contact_email}
        #
        #email.send()
        return super(MerchantApprovalForm, self).form_valid(form)

def MerchantApprovalFormLandingView(request):
    return render(request, 'portal/approval/merchant_approval_form_landing.html')
