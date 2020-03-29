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
                subscription = payments_models.Subscription.objects.get(subscription_id=test_subscription)
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

            subscription_qs = payments_models.Subscription.objects.filter(subscription_id=test_subscription)
            if subscription_qs.exists():
                subscription = payments_models.Subscription.objects.get(subscription_id=test_subscription)
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