import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.mail import send_mail

from django.utils.decorators import method_decorator

from users import models as users
from payments import models as payments_models

import stripe

# Using Django
@method_decorator(csrf_exempt, name='dispatch')
class TrialWebhook(View):

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), 
                stripe.api_key,
            )

            print(event)
            return HttpResponse()

        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'customer.subscription.created':
            customer_subscription_created = event.data.object

            send_mail('New Subscription Created!', 'There is a new subscription for your site. Please check it out.', 'michael@modwebservices.com', ['michael@modwebservices.com',])

            print(customer_subscription_created)
        if event.type == 'invoice.created':
            invoice_created = event.data.object
            print(invoice_created)        
        if event.type == 'invoice.finalized':
            invoice_finalized = event.data.object
            print(invoice_finalized)
        if event.type == 'charge.succeeded':
            charge_succeeded = event.data.object
            print(charge_succeeded)
        if event.type == 'invoice.payment_succeeded':
            invoice = event.data.object
        if event.type == 'customer.subscription.deleted':
            customer_subscription_deleted = event.data.object

            send_mail('Subscription Deleted!', 'There has been a subscription cancellation. Please check it out.', 'michael@modwebservices.com', ['michael@modwebservices.com',])

            print(customer_subscription_deleted)
        else:
            return HttpResponse(status=400)

        return HttpResponse(status=200)