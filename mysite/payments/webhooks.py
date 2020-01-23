import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from django.utils.decorators import method_decorator

import stripe

# Using Django
@method_decorator(csrf_exempt, name='dispatch')
class TrialWebhook(View):

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY_MPM
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
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            print(payment_intent)
        if event.type == 'invoice.payment_succeeded':
            invoice = event.data.object
            print(invoice)
        if event.type == 'invoice.finalized':
            invoice_finalized = event.data.object
            print(invoice_finalized)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
            print(payment_method)
        else:
        # Unexpected event type
            return HttpResponse(status=400)

        return HttpResponse(status=200)