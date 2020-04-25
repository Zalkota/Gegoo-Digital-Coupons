import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.mail import send_mail

from django.utils.decorators import method_decorator

from users import models as users
from payments import models as payments_models

import stripe
import datetime

STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

#TODO add to settings variable
endpoint_secret = 'whsec_vOpYDyI05NhPSnS2xuOmoCcu87jBcC6h'

stripe.api_key = STRIPE_SECRET_KEY

# Using Django 
@method_decorator(csrf_exempt, name='dispatch')
class TrialWebhook(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'payments/webhook.html')

    def post(self, request, *args, **kwargs):
        payload = self.request.body
        sig_header = self.request.META['HTTP_STRIPE_SIGNATURE']
        event = None


        try:
            event = stripe.Webhook.construct_event(
                payload, 
                sig_header,
                endpoint_secret,
            )
        except ValueError as e:
            # Invalid payload
            print(e)
            return HttpResponse(e)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(e)
            return HttpResponse(e)

        # Subscription Webhooks

        if event.type == 'invoice.upcoming':
            try:
                invoice_upcoming = event.data.object 

                customer_subscription = invoice_upcoming['lines']['data'][0].subscription

                sub = payments_models.Subscription.objects.get_or_create(subscription_id=customer_subscription)
                if sub.invoice_upcoming == False:
                    sub.invoice_upcoming = True
                    sub.save()
            except:
                print('Error')


        elif event.type == 'invoice.payment_succeeded':
            try:
                invoice_payment_succeeded = event.data.object 

                customer_subscription = invoice_payment_succeeded['lines']['data'][0].subscription

                subscription = stripe.Subscription.retrieve(
                    id = customer_subscription,
                    expand=['items', 'latest_invoice.payment_intent', 'plan'],
                )

                sub, created = payments_models.Subscription.objects.get_or_create(subscription_id=customer_subscription)
                
                creation_date = sub.created_at_date()
                todays_date = datetime.date.today()

                if creation_date != todays_date:

                    sub.subscription_id             = subscription['id']
                    sub.unix_current_period_start   = subscription['current_period_start']
                    sub.unix_current_period_end     = subscription['current_period_end']
                    sub.subscription_item_id        = subscription['items']['data'][0].id
                    sub.subscription_quantity       = subscription['items']['data'][0].quantity
                    sub.plan_id                     = subscription['plan']['id']
                    sub.subscription_status         = subscription['status']
                    sub.latest_invoice_id           = subscription['latest_invoice']['id']
                    sub.latest_invoice_number       = subscription['latest_invoice']['number']
                    sub.latest_invoice_status       = subscription['latest_invoice']['status']
                    sub.latest_invoice_url          = subscription['latest_invoice']['hosted_invoice_url']
                    sub.latest_receipt_url          = subscription['latest_invoice']['payment_intent']['charges']['data'][0].receipt_url
                    sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']

                    if sub.invoice_upcoming == True:
                        sub.invoice_upcoming = False

                    sub.save()
            except:
                print('Error')


        elif event.type == 'invoice.payment_failed':
            try:
                invoice_payment_failed = event.data.object 
                print(invoice_payment_failed)

                customer_subscription = invoice_payment_failed['lines']['data'][0].subscription

                subscription = stripe.Subscription.retrieve(
                    id = customer_subscription,
                    expand=['items', 'latest_invoice.payment_intent', 'plan'],
                )

                sub, created = payments_models.Subscription.objects.get_or_create(subscription_id=customer_subscription)

                creation_date = sub.created_at_date()
                todays_date = datetime.date.today()

                if sub.created_at_date() != todays_date:
                    sub.subscription_id             = subscription['id']
                    sub.unix_current_period_start   = subscription['current_period_start']
                    sub.unix_current_period_end     = subscription['current_period_end']
                    sub.subscription_item_id        = subscription['items']['data'][0].id
                    sub.subscription_quantity       = subscription['items']['data'][0].quantity
                    sub.plan_id                     = subscription['plan']['id']
                    sub.subscription_status         = subscription['status']
                    sub.latest_invoice_id           = subscription['latest_invoice']['id']
                    sub.latest_invoice_number       = subscription['latest_invoice']['number']
                    sub.latest_invoice_status       = subscription['latest_invoice']['status']
                    sub.latest_invoice_url          = subscription['latest_invoice']['hosted_invoice_url']
                    sub.latest_receipt_url          = subscription['latest_invoice']['payment_intent']['charges']['data'][0].receipt_url
                    sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']
                    
                    if sub.invoice_upcoming == True:
                        sub.invoice_upcoming = False

                    sub.save()
            except:
                print('Error')

        elif event.type == 'customer.subscription.trial_will_end':
            try:
                trial_will_end = event.data.object

                customer_subscription = trial_will_end['items']['data'][0].subscription

                sub = payments_models.Subscription.objects.get_or_create(subscription_id=customer_subscription)
                if sub.trial_will_end == False:
                    sub.trial_will_end = True
                    sub.save()
            except:
                print('Error')

        elif event.type == 'customer.subscription.updated':
            pass

        else:
            # Unexpected event type
            return HttpResponse(status=400)

        return HttpResponse(status=200)