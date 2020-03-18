from django.shortcuts import render, redirect, reverse, render_to_response
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView, View, UpdateView
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from payments import models as payments_models
from users import models as users_models
from payments import forms as payments_forms
from portal import models as portal_models
import json


#Stripe import key
STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY


def get_user_subscription(request):
    try:
        user_subscription_qs = payments_models.Subscription.objects.get(user=request.user)
        return user_subscription_qs
    except:
        pass


class PlanListView(ListView):
    model = payments_models.Plan
    template_name = 'payments/plan_list.html'

    def get_queryset(self):
        plan_list = payments_models.Plan.objects.all()
        return plan_list

class PlanDetailView(LoginRequiredMixin, DetailView):

    def get(self, *args, **kwargs):
        #Mimic Detail View
        slug = kwargs['slug']
        plan = payments_models.Plan.objects.get(slug=slug)

        #Obtain stores from user

        stores = portal_models.Store.objects.filter(merchant=self.request.user, subscription_status=False)
        print(stores)
        if not stores.exists():
            messages.success(self.request, "No inactive stores found, please create a store first")
            return redirect("/approval/store/create/")
        else:
            context = {
                'object': plan,
                'stores': stores,
                'STRIPE_PUB_KEY': STRIPE_PUB_KEY,
                'promotion_form': payments_forms.PromotionForm()
            }
            return render(self.request, 'payments/plan_detail.html', context)

    def post(self, *args, **kwargs):
        # Return Detail View Object
        slug = kwargs['slug']
        self.object = payments_models.Plan.objects.get(slug=slug)

        # Stripe API Calls
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = self.request.POST.get('stripeToken')

        # Customer Store Data
        customer = self.request.user.merchant_profile.customer_id
        customer_stores = self.request.user.merchant_profile.stores
        customer_store_qs = portal_models.Store.objects.filter(merchant=self.request.user, subscription_status=False)

        # Get Detail View Object
        plan = self.object.plan_id

        if payments_models.Subscription.objects.filter(user=self.request.user).exists():

            subscription = payments_models.Subscription.objects.get(user=self.request.user)

            if subscription.subscription_status == 'active':
                messages.warning(self.request, 'You already have an %s subscription' % subscription.subscription_status)
                return redirect('users:userPage')

            elif subscription.subscription_status == 'trialing':
                messages.warning(self.request, 'You are already %s a subscription' % subscription.subscription_status)
                return redirect('users:userPage')

            elif subscription.subscription_status == 'incomplete':
                messages.warning(self.request, 'Your subscription is %s. Please Adjust your payment info on the dashboard' % subscription.subscription_status)
                return redirect('users:userPage')

            elif subscription.subscription_status == 'canceled':
                if payments_models.PromoUser.objects.filter(user=self.request.user).exists():

                    promouser           = payments_models.PromoUser.objects.get(user=self.request.user)
                    promotion_plan_id   = promouser.promotion.plan.plan_id
                    promotion_period    = promouser.promotion.trial_period

                    if promotion_plan_id == plan:
                        if promouser.has_used == False:
                            try:
                                stripe.Customer.modify(
                                    customer,
                                    source=token,
                                )

                                subscription = stripe.Subscription.create(
                                    customer = customer,
                                    items = [
                                        {
                                            'plan': plan,
                                            'quantity': customer_stores,
                                        },
                                    ],
                                    trial_period_days = promotion_period,
                                    expand=['items', 'plan'],
                                )

                                promouser.has_used = True
                                promouser.save()

                                sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                                sub.subscription_id         = subscription['id']
                                sub.subscription_item_id    = subscription['items']['data'][0].id
                                sub.subscription_quantity   = subscription['items']['data'][0].quantity
                                sub.plan_id                 = subscription['plan']['id']
                                sub.subscription_status     = subscription['status']
                                sub.unix_trial_start        = subscription['trial_start']
                                sub.unix_trial_end          = subscription['trial_end']
                                sub.save()

                                # Get Stores and Set Status to paid
                                # TODO add trial option to store model
                                for each in customer_store_qs:
                                    item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                    item.subscription_status = True
                                    item.save()

                                messages.success(self.request, 'Your promotional code was accepted, and your Subscription Was Successful!')
                                return redirect('users:merchant_approval_videofile_list')

                                # subject = 'Subscription'
                                # context = {
                                #     'user': self.request.user,
                                #     'subscription': sub,
                                # }
                                # template = 'mail/email/email_base.html'
                                # html_message = render_to_string(template, context)
                                # msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
                                # msg.send()

                            except stripe.error.CardError as e:
                                messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                                return render(self.request, 'payments/plan_detail.html')

                        else:
                            try:
                                stripe.Customer.modify(
                                    customer,
                                    source=token,
                                )

                                subscription = stripe.Subscription.create(
                                    customer = customer,
                                    items = [
                                        {
                                            'plan': plan,
                                            'quantity': customer_stores,
                                        },
                                    ],
                                    expand=['items', 'latest_invoice.payment_intent', 'plan'],
                                )

                                sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                                sub.subscription_id         = subscription['id']
                                sub.subscription_item_id    = subscription['items']['data'][0].id
                                sub.subscription_quantity   = subscription['items']['data'][0].quantity
                                sub.plan_id                 = subscription['plan']['id']
                                sub.subscription_status     = subscription['status']
                                sub.latest_invoice_status   = subscription['latest_invoice']['status']
                                sub.payment_status          = subscription['latest_invoice']['payment_intent']['status']
                                sub.save()

                                if sub.payment_status == 'succeeded':
                                    # Get Stores and Set Payment Status
                                    for each in customer_store_qs:
                                        item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                        item.subscription_status = True
                                        item.save()

                                    messages.success(self.request, 'You have already used a promotional trial, but your subscription activation was successful!') #TODO ERROR HERE?
                                    return redirect('users:merchant_approval_videofile_list')

                                elif sub.payment_status == 'requires_payment_method':
                                    messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                                    return redirect('users:userPage')

                                else:
                                    messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                                    return render(self.request, 'payments/plan_detail.html')

                                # subject = 'Subscription'
                                # context = {
                                #     'user': self.request.user,
                                #     'subscription': sub,
                                # }
                                # template = 'mail/email/email_base.html'
                                # html_message = render_to_string(template, context)
                                # msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
                                # msg.send()

                            except stripe.error.CardError as e:
                                messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                                return render(self.request, 'payments/plan_detail.html')

                    else:
                        messages.warning(self.request, 'Please use a promotion for the plan you have selected. Please try again with a different promotion source!')
                        return render(self.request, 'payments/plan_detail.html')

                else:
                    try:
                        stripe.Customer.modify(
                            customer,
                            source=token,
                        )

                        subscription = stripe.Subscription.create(
                            customer = customer,
                            items = [
                                {
                                    'plan': plan,
                                    'quantity': customer_stores,
                                },
                            ],
                            expand=['items', 'latest_invoice.payment_intent', 'plan'],
                        )

                        sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                        sub.subscription_id         = subscription['id']
                        sub.subscription_item_id    = subscription['items']['data'][0].id
                        sub.subscription_quantity   = subscription['items']['data'][0].quantity
                        sub.plan_id                 = subscription['plan']['id']
                        sub.subscription_status     = subscription['status']
                        sub.latest_invoice_status   = subscription['latest_invoice']['status']
                        sub.payment_status          = subscription['latest_invoice']['payment_intent']['status']
                        sub.save()

                        if sub.payment_status == 'succeeded':
                            # Get Stores and Set Payment Status
                            for each in customer_store_qs:
                                item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                item.subscription_status = True
                                item.save()

                            messages.success(self.request, 'You have already used a promotional trial, but your subscription activation was successful!')
                            return redirect('users:merchant_approval_videofile_list')

                        elif sub.payment_status == 'requires_payment_method':
                            messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                            return redirect('users:userPage')

                        else:
                            messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                            return render(self.request, 'payments/plan_detail.html')

                        # subject = 'Subscription'
                        # context = {
                        #     'user': self.request.user,
                        #     'subscription': sub,
                        # }
                        # template = 'mail/email/email_base.html'
                        # html_message = render_to_string(template, context)
                        # msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
                        # msg.send()

                    except stripe.error.CardError as e:
                        messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                        return render(self.request, 'payments/plan_detail.html')

        else:

            if payments_models.PromoUser.objects.filter(user=self.request.user).exists():

                promouser           = payments_models.PromoUser.objects.get(user=self.request.user)
                promotion_plan_id   = promouser.promotion.plan.plan_id
                promotion_period    = promouser.promotion.trial_period

                if promotion_plan_id == plan:
                    if promouser.has_used == False:
                        try:
                            stripe.Customer.modify(
                                customer,
                                source=token,
                            )

                            subscription = stripe.Subscription.create(
                                customer = customer,
                                items = [
                                    {
                                        'plan': plan,
                                        'quantity': customer_stores,
                                    },
                                ],
                                trial_period_days = promotion_period,
                                expand=['items', 'plan'],
                            )

                            promouser.has_used = True
                            promouser.save()

                            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                            sub.subscription_id         = subscription['id']
                            sub.subscription_item_id    = subscription['items']['data'][0].id
                            sub.subscription_quantity   = subscription['items']['data'][0].quantity
                            sub.plan_id                 = subscription['plan']['id']
                            sub.subscription_status     = subscription['status']
                            sub.unix_trial_start        = subscription['trial_start']
                            sub.unix_trial_end          = subscription['trial_end']
                            sub.save()

                            messages.success(self.request, 'Your promotional code was accepted, and your Subscription Was Successful!')
                            return redirect('users:merchant_approval_videofile_list')

                            # subject = 'Subscription'
                            # context = {
                            #     'user': self.request.user,
                            #     'subscription': sub,
                            # }
                            # template = 'mail/email/email_base.html'
                            # html_message = render_to_string(template, context)
                            # msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
                            # msg.send()

                        except stripe.error.CardError as e:
                            messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                            return render(self.request, 'payments/plan_detail.html')

                    else:
                        try:
                            stripe.Customer.modify(
                                customer,
                                source=token,
                            )

                            subscription = stripe.Subscription.create(
                                customer = customer,
                                items = [
                                    {
                                        'plan': plan,
                                        'quantity': customer_stores,
                                    },
                                ],
                                expand=['items', 'latest_invoice.payment_intent', 'plan'],
                            )

                            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                            sub.subscription_id         = subscription['id']
                            sub.subscription_item_id    = subscription['items']['data'][0].id
                            sub.subscription_quantity   = subscription['items']['data'][0].quantity
                            sub.plan_id                 = subscription['plan']['id']
                            sub.subscription_status     = subscription['status']
                            sub.latest_invoice_status   = subscription['latest_invoice']['status']
                            sub.payment_status          = subscription['latest_invoice']['payment_intent']['status']
                            sub.save()

                            if sub.payment_status == 'succeeded':
                                # Get Stores and Set Payment Status
                                for each in customer_store_qs:
                                    item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                    item.subscription_status = True
                                    item.save()

                                messages.success(self.request, 'You have already used a promotional trial, but your subscription activation was successful!') #
                                return redirect('users:merchant_approval_videofile_list')

                            elif sub.payment_status == 'requires_payment_method':
                                messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                                return redirect('users:userPage')

                            else:
                                messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                                return render(self.request, 'payments/plan_detail.html')

                            # subject = 'Subscription'
                            # context = {
                            #     'user': self.request.user,
                            #     'subscription': sub,
                            # }
                            # template = 'mail/email/email_base.html'
                            # html_message = render_to_string(template, context)
                            # msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
                            # msg.send()

                        except stripe.error.CardError as e:
                            messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                            return render(self.request, 'payments/plan_detail.html')

                else:
                    messages.warning(self.request, 'Please use a promotion for the plan you have selected. Please try again with a different promotion source!')
                    return render(self.request, 'payments/plan_detail.html')

            else:
                try:
                    stripe.Customer.modify(
                        customer,
                        source=token,
                    )

                    subscription = stripe.Subscription.create(
                        customer = customer,
                        items = [
                            {
                                'plan': plan,
                                'quantity': customer_stores,
                            },
                        ],
                        expand=['items', 'latest_invoice.payment_intent', 'plan'],
                    )

                    sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                    sub.subscription_id         = subscription['id']
                    sub.subscription_item_id    = subscription['items']['data'][0].id
                    sub.subscription_quantity   = subscription['items']['data'][0].quantity
                    sub.plan_id                 = subscription['plan']['id']
                    sub.subscription_status     = subscription['status']
                    sub.latest_invoice_status   = subscription['latest_invoice']['status']
                    sub.payment_status          = subscription['latest_invoice']['payment_intent']['status']
                    sub.save()

                    if sub.payment_status == 'succeeded':
                        # Get Stores and Set Payment Status
                        for each in customer_store_qs:
                            item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                            item.subscription_status = True
                            item.save()

                        messages.success(self.request, 'You have already used a promotional trial, but your subscription activation was successful!')
                        return redirect('users:merchant_approval_videofile_list')

                    elif sub.payment_status == 'requires_payment_method':
                        messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                        return redirect('users:userPage')

                    else:
                        messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                        return render(self.request, 'payments/plan_detail.html')

                    # subject = 'Subscription'
                    # context = {
                    #     'user': self.request.user,
                    #     'subscription': sub,
                    # }
                    # template = 'mail/email/email_base.html'
                    # html_message = render_to_string(template, context)
                    # msg = EmailMessage(subject, html_message, to=['michael@modwebservices.com', ], from_email='michael@modwebservices.com')
                    # msg.send()

                except stripe.error.CardError as e:
                    messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                    return render(self.request, 'payments/plan_detail.html')

class Charge(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'payments/charge.html')

class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    model = payments_models.Subscription
    template_name = 'payments/subscription_detail.html'

    def get_queryset(self):
        return payments_models.Subscription.objects.filter(user=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(SubscriptionDetailView, self).get_context_data(**kwargs)
    #     context['stores'] = portal_models.Store.objects.filter(merchant=self.request.user)
    #     return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key          = settings.STRIPE_SECRET_KEY
        subscription_id         = self.object.subscription_id
        subscription_item_id    = self.object.subscription_item_id
        subscription_quantity   = self.object.subscription_quantity
        customer_stores         = self.request.user.merchant_profile.stores

        # Customer has added a store
        if customer_stores > subscription_quantity:
            if 'upgrade' in request.POST:

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
                messages.warning(self.request, 'Your Subscription cannot be upgraded at this time. Please contact support.')
                return render(self.request, 'payments/subscription_detail.html')

        elif customer_stores < subscription_quantity:
            if 'downgrade' in request.POST:

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

                messages.success(self.request, 'Your Subscription downgrade Was Successful!')
                return redirect('payments:plan_list')
            else:
                messages.warning(self.request, 'Your Subscription cannot be downgraded at this time. Please contact support.')
                return render(self.request, 'payments/subscription_detail.html')

        else:
            if 'delete' in request.POST:
                subscription = stripe.Subscription.delete(
                    subscription_id,
                    expand=['items', 'plan'],
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
            else:
                messages.warning(self.request, 'Your Subscription cannot be cancelled at this time. Please contact support.')
                return render(self.request, 'payments/subscription_detail.html')

class UpdatePaymentInformation(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payments/charge.html')

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = self.request.POST.get('stripeToken')
        customer = self.request.user.merchant_profile.customer_id

        stripe.Customer.modify(
            customer,
            source=token,
        )

def ApplyPromo(request):
    if request.method == 'POST':
        form = payments_forms.PromotionForm(request.POST)
        if form.is_valid():
            try:
                code                = form.cleaned_data['code']
                promo               = payments_models.Promotion.objects.get(code__iexact=code)
                promo_qs            = payments_models.PromoUser.objects.filter(user=request.user, promotion=promo)

                if promo_qs.exists():
                    messages.warning(request, 'You have already applied %s!' % promo.code)
                    return redirect('payments:plan_detail', slug=promo.plan.slug)

                promouser = payments_models.PromoUser.objects.create(user=request.user, promotion=promo)
                promouser.save()

                messages.success(request, 'You Have Successfully applied %s' % promo.code)
                return redirect('payments:plan_detail', slug=promo.plan.slug)

            except:
                messages.warning(request, 'Promotion not found. Please enter the code again and or contact support.')
                return redirect('payments:plan_detail', slug='gegoo-basic-subscription')

    else:
        return redirect('payments:plan_detail', slug='gegoo-basic-subscription')
