from django.shortcuts import render

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Merchant
from django.views.generic import ListView, DetailView, View
# Create your views here.

def get_user_orders(request, user):
	user_orders_qs = Order.objects.filter(user=user)
	if user_orders_qs.exists():
		return user_orders_qs
	return None



class MerchantDetailView(View):

    def get(self, *args, **kwargs):
        try:
            merchant = Merchant.objects.get(ref_code=self.kwargs['ref_code'])

            context = {
            'merchant': merchant
            }
            return render(self.request, "portal/merchant_detail.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "Error contact admin")
            return redirect("home-page")


    #def post(self, *args, **kwargs):

    #return redirect("/payment/stripe/")
