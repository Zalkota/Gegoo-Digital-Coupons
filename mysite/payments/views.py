from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView, View, UpdateView
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
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key = settings.STRIPE_SECRET_KEY_MPM
        token = self.request.POST.get('stripeToken')
        customer = self.request.user.merchant_profile.customer_id
        plan = self.object.plan_id

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
                expand=['items', 'latest_invoice', 'plan'],
            )

            print(subscription['items']['data'][0].id)

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.payment_intent_status   = subscription['latest_invoice']['payment_intent']
            sub.save()

            messages.success(self.request, 'Your Subscription Was Successful!')
            return redirect('payments:charge')

        except stripe.error.CardError as e:
            print('Status is: %s' % e.http_status)


class Charge(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'payments/charge.html')

class SubscriptionDetailView(DetailView):
    model = payments_models.Subscription
    template_name = 'payments/subscription_detail.html'

    def get_queryset(self):
        return payments_models.Subscription.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(**kwargs)
        context['plans'] = payments_models.Plan.objects.exclude(plan_id = self.request.user.subscription.plan_id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key          = settings.STRIPE_SECRET_KEY_MPM
        subscription_id         = self.request.user.subscription.subscription_id
        subscription_item_id    = self.request.user.subscription.subscription_item_id
        print(subscription_id)

        if 'delete' in request.POST:
            subscription = stripe.Subscription.delete(
                subscription_id,
                expand=['items', 'latest_invoice', 'plan'],
            )

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.save()
            
            messages.success(self.request, 'Your Subscription Cancellation Was Successful!')
            return redirect('payments:plan_list')
        
        elif 'upgrade' in request.POST:
            context = self.get_context_data(**kwargs)
            
            subscription = stripe.Subscription.modify(
                subscription_id,
                items = [{
                    'id': subscription_item_id,
                    'plan': context['plans'].first().plan_id,
                }],
            )

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.save()
            
            messages.success(self.request, 'Your Subscription Upgrade Was Successful!')
            return redirect('payments:plan_list')

        else:
            pass