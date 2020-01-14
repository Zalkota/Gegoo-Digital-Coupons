# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from portal import models as portal_models
from users import models as users_models
from .forms import MerchantProfileForm
from django.views.generic.edit import FormView, FormMixin
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from location.functions import set_location_cookies, get_ip, get_or_set_location
from users.decorators import user_is_merchant



class MerchantProfileUpdateView(UpdateView):
    form_class = MerchantProfileForm
    model = users_models.MerchantProfile
    success_url = reverse_lazy('merchant-profile-landing-page')
    template_name = 'users/approval/merchant_profile_update.html'


    def form_valid(self, form):
        MerchantProfileForm = form.save(commit=False)
        MerchantProfileForm.business_name = form.cleaned_data['business_name']
        MerchantProfileForm.description = form.cleaned_data['description']
        MerchantProfileForm.phone_number = form.cleaned_data['phone_number']
        MerchantProfileForm.street_address = form.cleaned_data['street_address']
        MerchantProfileForm.city = form.cleaned_data['city']
        MerchantProfileForm.state = form.cleaned_data['state']
        MerchantProfileForm.zip = form.cleaned_data['zip']
        MerchantProfileForm.website_url = form.cleaned_data['website_url']
        MerchantProfileForm.facebook_url = form.cleaned_data['facebook_url']
        MerchantProfileForm.status = 'PENDING'
        MerchantProfileForm.save()


        #send_email(ContactForm.name, ContactForm.email, ContactForm.phone, ContactForm.description)

        return super(MerchantProfileUpdateView, self).form_valid(form)

def MerchantProfileFormLandingView(request):
    return render(request, 'users/approval/merchant_profile_form_landing.html')
