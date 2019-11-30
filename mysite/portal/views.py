from django.shortcuts import render
from .models import Merchant
from django.views.generic import ListView, DetailView, View
# Create your views here.



class MerchantDetailView(View):

    def get(self, *args, **kwargs):
        merchant = Merchant.objects.filter(ref_code=self.kwargs['ref_code'])

        return render(self.request, "portal/merchant_detail.html", context)

    #def post(self, *args, **kwargs):

    #return redirect("/payment/stripe/")
