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

STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY_TEST
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY_TEST

# Using Django
@method_decorator(csrf_exempt, name='dispatch')
class TrialWebhook(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'payments/webhook.html')

    def post(self, request, *args, **kwargs):
        payload = self.request.body
        event = None

        stripe.api_key = STRIPE_SECRET_KEY

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), 
                stripe.api_key,
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(e)

        # Subscription Webhooks

        if event.type == 'invoice.upcoming':
            invoice_upcoming = event.data.object 
            print(invoice_upcoming)

            customer_subscription = invoice_upcoming['lines']['data'][0].subscription
            print(customer_subscription)

            test_subscription = 'sub_H02Niv3sSCCVyT'

            # Currently using test subscription - Test events sent with random subscriptions
            subscription_qs = payments_models.Subscription.objects.filter(subscription_id=test_subscription)
            if subscription_qs.exists():
                subscription = subscription_qs.first()
                if subscription.invoice_upcoming == False:
                    subscription.invoice_upcoming = True
                else:
                    pass
                subscription.save()
                print(subscription.invoice_upcoming)
            else:
                print('Sub doesnt exist')


        elif event.type == 'invoice.payment_succeeded':
            invoice_payment_succeeded = event.data.object 
            print(invoice_payment_succeeded)

            customer_subscription = invoice_payment_succeeded['lines']['data'][0].subscription
            print(customer_subscription)

            test_subscription = 'sub_H02Niv3sSCCVyT'

            stripe_subscription_api_call = stripe.Subscription.retrieve(
                id = test_subscription,
                expand=['items', 'latest_invoice.payment_intent', 'plan'],
            )

            print('retrieve start')
            print(stripe_subscription_api_call)
            print('retrieve end')  

            # Update subscription info #TODO
            # sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            # sub.subscription_id             = subscription['id']
            # sub.unix_current_period_start   = subscription['current_period_start']
            # sub.unix_current_period_end     = subscription['current_period_end']
            # sub.subscription_item_id        = subscription['items']['data'][0].id
            # sub.subscription_quantity       = subscription['items']['data'][0].quantity
            # sub.plan_id                     = subscription['plan']['id']
            # sub.subscription_status         = subscription['status']
            # sub.latest_invoice_id           = subscription['latest_invoice']['id']
            # sub.latest_invoice_number       = subscription['latest_invoice']['number']
            # sub.latest_invoice_status       = subscription['latest_invoice']['status']
            # sub.latest_invoice_url          = subscription['latest_invoice']['hosted_invoice_url']
            # sub.latest_receipt_url          = subscription['latest_invoice']['payment_intent']['charges']['data'][0].receipt_url
            # sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']
            # sub.save()

            subscription_qs = payments_models.Subscription.objects.filter(subscription_id=test_subscription)
            if subscription_qs.exists():
                subscription = subscription_qs.first()
                if subscription.invoice_upcoming == True:
                    subscription.invoice_upcoming = False
                else:
                    pass
                subscription.save()
                print(subscription.invoice_upcoming)
            else:
                print('Sub doesnt exist')


        else:
            # Unexpected event type
            return HttpResponse(status=400)

        return HttpResponse(status=200)