# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from portal import models as portal_models
from users import models as users_models
from files import models as files_models
from django.utils.text import slugify
from django.views.generic.edit import FormView, FormMixin
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from location.functions import set_location_cookies, get_ip, get_or_set_location
from users.decorators import user_is_merchant
from django.contrib.auth.mixins import LoginRequiredMixin
from portal.forms import MerchantStoreForm

#
# class MerchantProfileUpdateView(LoginRequiredMixin, UpdateView):
#     form_class = MerchantProfileForm
#     model = users_models.MerchantProfile
#     success_url = reverse_lazy('merchant_approval_store_create')
#     template_name = 'users/approval/merchant_profile_update.html'
#
#
#     def form_valid(self, form):
#         MerchantProfileForm = form.save(commit=False)
#         MerchantProfileForm.business_name = form.cleaned_data['business_name']
#         MerchantProfileForm.phone_number = form.cleaned_data['phone_number']
#         MerchantProfileForm.street_address = form.cleaned_data['street_address']
#         MerchantProfileForm.city = form.cleaned_data['city']
#         MerchantProfileForm.state = form.cleaned_data['state']
#         MerchantProfileForm.zip = form.cleaned_data['zip']
#         MerchantProfileForm.website_url = form.cleaned_data['website_url']
#         MerchantProfileForm.facebook_url = form.cleaned_data['facebook_url']
#         MerchantProfileForm.status = 'PENDING'
#         MerchantProfileForm.save()
#
#
#         #send_email(ContactForm.name, ContactForm.email, ContactForm.phone, ContactForm.description)
#
#         return super(MerchantProfileUpdateView, self).form_valid(form)
#
def MerchantApprovalAdditionalStoreView(request):
    return render(request, 'users/approval/merchant_approval_additional_store.html')


class MerchantApprovalStoreCreateView(LoginRequiredMixin, CreateView):
    model = portal_models.Store
    form_class = MerchantStoreForm
    template_name = 'users/approval/merchant_approval_store_create.html'
    success_message = "Step Two: Complete!"
    success_url = reverse_lazy('users:merchant_approval_additional_store')

    def get_context_data(self, **kwargs):
        context = super(MerchantApprovalStoreCreateView, self).get_context_data(**kwargs)
        context['store_list'] = portal_models.Store.objects.filter(merchant=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user

        #Set user status as pending
        user.status = 'PENDING'
        user.save()

        #Set stores owner
        form.instance.merchant = user

        #Set Store Slug as business name and city combined
        business_name = form.cleaned_data.get('business_name')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        ref_code = portal_models.random_string_generator()
        string = business_name + '-' + city + '-' + state + '-' + ref_code
        slug = slugify(string)
        form.instance.ref_code = ref_code
        form.instance.slug = slug

        return super(MerchantApprovalStoreCreateView, self).form_valid(form)


class MerchantApprovalVideoFileListView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            store_qs = portal_models.Store.objects.filter(merchant=self.request.user)
            context = {
                'store_list': store_qs
            }

            return render(self.request, 'users/approval/merchant_approval_video_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "No Stores Found, Please create a store")
            return redirect("/dashboard/")
