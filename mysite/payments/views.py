from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView, View, UpdateView
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from payments import models as payments_models
from users import models as users_models
from payments import forms as payments_forms
from portal import models as portal_models

import json

class PlanListView(ListView):
    model = payments_models.Plan
    template_name = 'payments/plan_list.html'

    def get_queryset(self):
        plan_list = payments_models.Plan.objects.all()
        return plan_list



class PlanDetailView(LoginRequiredMixin, DetailView):
    model = payments_models.Plan
    template_name = 'payments/plan_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        context['coupon_apply_form'] = payments_forms.ApplyCouponForm()
        context['stores'] = portal_models.Store.objects.filter(merchant=self.request.user).all()
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key = settings.STRIPE_SECRET_KEY_MPM
        token = self.request.POST.get('stripeToken')
        customer = self.request.user.merchant_profile.customer_id
        customer_stores = self.request.user.merchant_profile.stores
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
                    'quantity': customer_stores,
                }],
                expand=['items', 'latest_invoice', 'plan'],
            )

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.subscription_quantity   = subscription['items']['data'][0].quantity
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.payment_intent_status   = subscription['latest_invoice']['payment_intent']
            sub.save()

            subject = 'Subscription'
            context = {
                'user': self.request.user,
                'subscription': sub,
            }
            template = 'mail/email/email_base.html'
            html_message = render_to_string(template, context)
            msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
            msg.send()

            # send_mail('Subscription', 'Your subscription was successful!', 'michael@modwebservices.com', ['michael@modwebservices.com',])

            messages.success(self.request, 'Your Subscription Was Successful!')
            return redirect('payments:charge')

        except stripe.error.CardError as e:
            print('Status is: %s' % e.http_status)


class Charge(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'payments/charge.html')

class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    model = payments_models.Subscription
    template_name = 'payments/subscription_detail.html'

    def get_queryset(self):
        return payments_models.Subscription.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key          = settings.STRIPE_SECRET_KEY_MPM
        subscription_id         = self.object.subscription_id
        subscription_item_id    = self.object.subscription_item_id
        customer_stores         = self.request.user.merchant_profile.stores

        if 'delete' in request.POST:
            subscription = stripe.Subscription.delete(
                subscription_id,
                expand=['items', 'latest_invoice', 'plan'],
            )

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.subscription_quantity   = subscription['items']['data'][0].quantity
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.save()

            messages.success(self.request, 'Your Subscription Cancellation Was Successful!')
            return redirect('payments:plan_list')

        elif 'upgrade' in request.POST:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
                items = [{
                    'id': subscription_item_id,
                    'plan': self.object.plan_id,
                    'quantity': customer_stores,
                }],
                proration_behavior='none',
            )

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.subscription_quantity   = subscription['items']['data'][0].quantity
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.save()

            messages.success(self.request, 'Your Subscription Upgrade Was Successful!')
            return redirect('payments:plan_list')

        else:
            pass

class PaymentIntent(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'payments/payment_intent.html')

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY_MPM
        subscription = self.request.user.subscription.subscription_id
        payment_intent = self.request.user.subscription.payment_intent_status

        try:
            sub = stripe.Subscription.retrieve(
                subscription,
                expand=['latest_invoice'],
            )

            pi = stripe.PaymentIntent.retrieve(
                sub['latest_invoice']['payment_intent'],
            )


            send_mail('Subscription', 'Your subscription was successful!', 'michael@modwebservices.com', ['michael@modwebservices.com',])

            print(sub['latest_invoice']['payment_intent'])
            print(pi['status'])
            return redirect('payments:payment_intent')

        except:
            pass

def ApplyPromo(request):
    if request.method == 'POST':
        form = payments_forms.ApplyCouponForm(request.POST)
        if form.is_valid():
            try:
                code                = form.cleaned_data['code']
                promo               = payments_models.Promotion.objects.get(code__iexact=code)
                promouser, created  = payments_models.PromoUser.objects.get_or_create(user=request.user, promotion=promo)
                promouser.times_used += 1
                promouser.save()

                print(promo)
                print(code)
                print(promouser)

                return HttpResponse('Success!')
            except:
                return HttpResponse('Failed!')

    

