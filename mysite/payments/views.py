from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib import messages
import stripe

from payments import models as payments_models
from users import models as users_models

import json

class PlanListView(ListView):
    model = payments_models.Plan
    template_name = 'payments/plan_list.html'

    def get_queryset(self):
        plan_list = payments_models.Plan.objects.all()
        return plan_list


class PlanDetailView(DetailView):
    model = payments_models.Plan
    template_name = 'payments/plan_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        context['merchantprofile'] = users_models.MerchantProfile.objects.get(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key = settings.STRIPE_SECRET_KEY_MPM
        token = self.request.POST.get('stripeToken')
        customer = self.request.user.merchant_profile.customer_id
        plan = self.object.plan_id
        print(customer)
        print(plan)

        try:
            stripe.Customer.modify(
			  customer,
			  source=token,
			)

            subscription = stripe.Subscription.create(
                customer = customer,
                items = [{
                    'plan': plan,
                }],
                expand=['latest_invoice.payment_intent'],
            )

            sub, created            = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id     = subscription['id']
            sub.subscription_status = subscription['status']
            sub.save()

            messages.success(self.request, 'Your Subscription Was Successful!')
            return redirect('payments:charge')

        except stripe.error.CardError as e:
            print('Status is: %s' % e.http_status)


class Charge(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'payments/charge.html')
