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
STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY_TEST
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY_TEST

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

    def get(self, request, *args, **kwargs):
        #Mimic Detail View
        slug = kwargs['slug']
        plan = payments_models.Plan.objects.get(slug=slug)
        stripe_pub_key = STRIPE_PUB_KEY

        #Obtain stores from user
        stores = portal_models.Store.objects.filter(merchant=self.request.user, subscription_status=False).order_by('created_at')

        # Get payment total
        total = plan.get_total() * self.request.user.merchant_profile.stores

        if not stores.exists():
            messages.success(self.request, "No inactive stores found, please create a store first")
            return redirect("/approval/store/create/")

        else:
            context = {
                'total': total,
                'object': plan,
                'stores': stores,
                'STRIPE_PUB_KEY': STRIPE_PUB_KEY,
                'promotion_form': payments_forms.PromotionForm()
            }
            return render(self.request, 'payments/plan_detail.html', context)

    def post(self, request, *args, **kwargs):
        # Return Detail View Object
        slug = kwargs['slug']
        self.object = payments_models.Plan.objects.get(slug=slug)

        # Stripe API Calls
        stripe.api_key = STRIPE_SECRET_KEY
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

            elif subscription.subscription_status == 'canceled' or subscription.subscription_status == 'incomplete_expired':
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
                                sub.unix_created_at         = subscription['created']
                                sub.subscription_item_id    = subscription['items']['data'][0].id
                                sub.subscription_quantity   = subscription['items']['data'][0].quantity
                                sub.plan_id                 = subscription['plan']['id']
                                sub.subscription_status     = subscription['status']
                                sub.unix_trial_start        = subscription['trial_start']
                                sub.unix_trial_end          = subscription['trial_end']
                                sub.save()
                                
                                # Set stores to be viewed on homepage after subscription success
                                for each in customer_store_qs:
                                    item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                    item.subscription_status = True
                                    item.save()

                                messages.success(self.request, 'Your promotional code was accepted. Your account status is now %s, and your Subscription Was Successful!') % self.request.user.merchant_profile.status
                                return redirect('payments:charge')

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

                                sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                                sub.subscription_id             = subscription['id']
                                sub.unix_created_at             = subscription['created']
                                sub.unix_current_period_start   = subscription['current_period_start']
                                sub.unix_current_period_end     = subscription['current_period_end']
                                sub.subscription_item_id        = subscription['items']['data'][0].id
                                sub.subscription_quantity       = subscription['items']['data'][0].quantity
                                sub.plan_id                     = subscription['plan']['id']
                                sub.subscription_status         = subscription['status']
                                sub.latest_invoice_status       = subscription['latest_invoice']['status']
                                sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']
                                sub.save()

                                if sub.payment_status == 'succeeded':

                                    if self.request.user.merchant_profile.status == 'INITIAL':
                                        merchant_profile_user = users_models.MerchantProfile.objects.get(user=self.request.user)
                                        merchant_profile_user.status = 'PENDING'
                                        merchant_profile_user.save()
                                    else:
                                        pass

                                    # Get Stores and Set Payment Status
                                    for each in customer_store_qs:
                                        item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                        item.subscription_status = True
                                        item.save()

                                    messages.success(self.request, 'You have already used a promotional trial, but your subscription activation was successful!') #TODO ERROR HERE?
                                    return redirect('payments:charge')

                                elif sub.payment_status == 'requires_payment_method':
                                    messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                                    return redirect('users:userPage')

                                else:
                                    messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                                    return render(self.request, 'payments/plan_detail.html')

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

                        sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                        sub.subscription_id             = subscription['id']
                        sub.unix_created_at             = subscription['created']
                        sub.unix_current_period_start   = subscription['current_period_start']
                        sub.unix_current_period_end     = subscription['current_period_end']
                        sub.subscription_item_id        = subscription['items']['data'][0].id
                        sub.subscription_quantity       = subscription['items']['data'][0].quantity
                        sub.plan_id                     = subscription['plan']['id']
                        sub.subscription_status         = subscription['status']
                        sub.latest_invoice_status       = subscription['latest_invoice']['status']
                        sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']
                        sub.save()

                        if sub.payment_status == 'succeeded':
                            # Get Stores and Set Payment Status
                            for each in customer_store_qs:
                                item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                item.subscription_status = True
                                item.save()

                            messages.success(self.request, 'Your subscription activation was successful!')
                            return redirect('payments:charge')

                        elif sub.payment_status == 'requires_payment_method':
                            messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                            return redirect('payments:payment_method_manage')

                        else:
                            messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                            return render(self.request, 'payments/plan_detail.html')

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

                            if self.request.user.merchant_profile.status == 'INITIAL':
                                merchant_profile_user = users_models.MerchantProfile.objects.get(user=self.request.user)
                                merchant_profile_user.status = 'PENDING'
                                merchant_profile_user.save()
                            else:
                                pass

                            messages.success(self.request, 'Your promotional code was accepted, and your Subscription Was Successful!')
                            return redirect('payments:charge')

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

                            sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                            sub.subscription_id             = subscription['id']
                            sub.unix_created_at             = subscription['created']
                            sub.unix_current_period_start   = subscription['current_period_start']
                            sub.unix_current_period_end     = subscription['current_period_end']
                            sub.subscription_item_id        = subscription['items']['data'][0].id
                            sub.subscription_quantity       = subscription['items']['data'][0].quantity
                            sub.plan_id                     = subscription['plan']['id']
                            sub.subscription_status         = subscription['status']
                            sub.latest_invoice_status       = subscription['latest_invoice']['status']
                            sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']
                            sub.save()

                            if sub.payment_status == 'succeeded':
                                if self.request.user.merchant_profile.status == 'INITIAL':
                                    merchant_profile_user = users_models.MerchantProfile.objects.get(user=self.request.user)
                                    merchant_profile_user.status = 'PENDING'
                                    merchant_profile_user.save()
                                else:
                                    pass

                                # Get Stores and Set Payment Status
                                for each in customer_store_qs:
                                    item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                                    item.subscription_status = True
                                    item.save()

                                messages.success(self.request, 'You have already used a promotional trial, but your subscription activation was successful!')
                                return redirect('payments:charge')

                            elif sub.payment_status == 'requires_payment_method':
                                messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                                return redirect('payments:payment_method_manage')

                            else:
                                messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                                return render(self.request, 'payments/plan_detail.html')

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

                    sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                    sub.subscription_id             = subscription['id']
                    sub.unix_created_at             = subscription['created']
                    sub.unix_current_period_start   = subscription['current_period_start']
                    sub.unix_current_period_end     = subscription['current_period_end']
                    sub.subscription_item_id        = subscription['items']['data'][0].id
                    sub.subscription_quantity       = subscription['items']['data'][0].quantity
                    sub.plan_id                     = subscription['plan']['id']
                    sub.subscription_status         = subscription['status']
                    sub.latest_invoice_status       = subscription['latest_invoice']['status']
                    sub.payment_status              = subscription['latest_invoice']['payment_intent']['status']
                    sub.save()

                    if sub.payment_status == 'succeeded':
                        if self.request.user.merchant_profile.status == 'INITIAL':
                            merchant_profile_user = users_models.MerchantProfile.objects.get(user=self.request.user)
                            merchant_profile_user.status = 'PENDING'
                            merchant_profile_user.save()
                        else:
                            pass

                        for each in customer_store_qs:
                            item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                            item.subscription_status = True
                            item.save()

                        messages.success(self.request, 'Your subscription activation was successful!')
                        return redirect('payments:charge')

                    elif sub.payment_status == 'requires_payment_method':
                        messages.warning(self.request, 'Your subscription was activated, but your card returned a payment error. Please update in the dashboard.')
                        return redirect('payments:payment_method_manage')
                    else:
                        messages.warning(self.request, 'Your charge didnt return a response, Please retry')
                        return render(self.request, 'payments/plan_detail.html')

                except stripe.error.CardError as e:
                    messages.warning(self.request, 'Something went wrong. Please try again with a different payment source! - status %s' % e.http_status)
                    return render(self.request, 'payments/plan_detail.html')

class Charge(View):

    def get(self, request, *args, **kwargs):
        subscription_qs = payments_models.Subscription.objects.filter(user=self.request.user)

        if subscription_qs.exists():
            subscription = payments_models.Subscription.objects.get(user=self.request.user)

            context = {
                'subscription': subscription
            }

            return render(self.request, 'payments/charge.html', context)
        else:
            error_message = 'You have to purchase a subscription to view this page'
            messages.warning(self.request, error_message)
            return redirect('users:userPage')

class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    model = payments_models.Subscription
    template_name = 'payments/subscription_detail_mpm.html'

    def get_queryset(self):
        return payments_models.Subscription.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        stripe.api_key          = STRIPE_SECRET_KEY
        subscription_id         = self.object.subscription_id

        customer_store_qs = portal_models.Store.objects.filter(merchant=self.request.user, subscription_status=True)

        if 'delete' in request.POST:
            subscription = stripe.Subscription.delete(
                subscription_id,
                expand=['items', 'plan'],
            )

            sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
            sub.subscription_id         = subscription['id']
            sub.unix_canceled_at        = subscription['canceled_at']
            sub.subscription_item_id    = subscription['items']['data'][0].id
            sub.subscription_quantity   = subscription['items']['data'][0].quantity
            sub.plan_id                 = subscription['plan']['id']
            sub.subscription_status     = subscription['status']
            sub.save()

            for each in customer_store_qs:
                item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                item.subscription_status = False
                item.save()

            messages.success(self.request, 'Your Subscription Cancellation Was Successful!')
            return redirect('users:userPage')
        else:
            messages.warning(self.request, 'Your Subscription cannot be cancelled at this time. Please contact support.')
            return render(self.request, 'payments/subscription_detail.html')


class SubscriptionManageView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        subscription_qs = payments_models.Subscription.objects.filter(user=self.request.user)

        if subscription_qs.exists():
            subscription = payments_models.Subscription.objects.get(user=self.request.user)
            plan = payments_models.Plan.objects.get(plan_id=subscription.plan_id)

        customer_store_qs = portal_models.Store.objects.filter(merchant=self.request.user, subscription_status=False).order_by('created_at')

        current_monthly_total = subscription.subscription_quantity * plan.get_total()
        new_payment_total = plan.get_total() * self.request.user.merchant_profile.stores

        context = {
            'subscription': subscription,
            'plan': plan,
            'new_payment_total': new_payment_total,
            'current_monthly_total': current_monthly_total,
            'stores': customer_store_qs,
        }

        if self.request.user.merchant_profile.stores > subscription.subscription_quantity:
            if self.request.user.merchant_profile.stores > 0:
                return render(self.request, 'payments/subscription_manage.html', context)
            else:
                error_message = 'You have deleted all your stores. Please cancel your subscription if there are no active stores!'
                messages.warning(self.request, error_message)
                return redirect('payments:subscription_detail', slug=subscription.slug)
        elif self.request.user.merchant_profile.stores < subscription.subscription_quantity:
            if self.request.user.merchant_profile.stores > 0:
                return render(self.request, 'payments/subscription_manage.html', context)
            else:
                error_message = 'You have deleted all your stores. Please cancel your subscription if there are no active stores!'
                messages.warning(self.request, error_message)
                return redirect('payments:subscription_detail', slug=subscription.slug)
        elif self.request.user.merchant_profile.stores == subscription.subscription_quantity:
            if self.request.user.merchant_profile.stores > 0:
                return render(self.request, 'payments/subscription_manage.html', context)
            else:
                error_message = 'You have deleted all your stores. Please cancel your subscription if there are no active stores!'
                messages.warning(self.request, error_message)
                return redirect('payments:subscription_detail', slug=subscription.slug)
        else:
            messages.warning(self.request, 'No subscription update is needed!')
            return redirect('users:userPage')

    def post(self, request, *args, **kwargs):
        subscription = payments_models.Subscription.objects.get(user=self.request.user)
        plan = payments_models.Plan.objects.get(plan_id=subscription.plan_id)

        customer_store_qs = portal_models.Store.objects.filter(merchant=self.request.user, subscription_status=False)

        stripe.api_key          = STRIPE_SECRET_KEY
        subscription_id         = subscription.subscription_id
        subscription_item_id    = subscription.subscription_item_id
        plan_id                 = plan.plan_id
        subscription_quantity   = subscription.subscription_quantity
        customer_stores         = self.request.user.merchant_profile.stores

        # Customer has added a store
        if 'upgrade' in request.POST:
            if customer_stores > subscription_quantity or customer_stores == subscription_quantity:

                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=False,
                    items = [{
                        'id': subscription_item_id,
                        'plan': plan_id,
                        'quantity': customer_stores,
                    }],
                    proration_behavior='none',
                )

                sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                sub.subscription_id             = subscription['id']
                sub.unix_current_period_start   = subscription['current_period_start']
                sub.unix_current_period_end     = subscription['current_period_end']
                sub.subscription_item_id        = subscription['items']['data'][0].id
                sub.subscription_quantity       = subscription['items']['data'][0].quantity
                sub.plan_id                     = subscription['plan']['id']
                sub.subscription_status         = subscription['status']
                sub.save()

                for each in customer_store_qs:
                    item = portal_models.Store.objects.get(merchant=self.request.user, slug=each.slug)
                    item.subscription_status = True
                    item.save()

                messages.success(self.request, 'Your Subscription Upgrade Was Successful!')
                return redirect('payments:charge')
            else:
                messages.warning(self.request, 'Your Subscription cannot be upgraded at this time. Please contact support.')
                return render(self.request, 'payments/subscription_manage.html')

        elif 'downgrade' in request.POST:
            if customer_stores < subscription_quantity:

                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=False,
                    items = [{
                        'id': subscription_item_id,
                        'plan': plan_id,
                        'quantity': customer_stores,
                    }],
                    proration_behavior='none',
                )

                sub, created                    = payments_models.Subscription.objects.get_or_create(user=self.request.user)
                sub.subscription_id             = subscription['id']
                sub.unix_current_period_start   = subscription['current_period_start']
                sub.unix_current_period_end     = subscription['current_period_end']
                sub.subscription_item_id        = subscription['items']['data'][0].id
                sub.subscription_quantity       = subscription['items']['data'][0].quantity
                sub.plan_id                     = subscription['plan']['id']
                sub.subscription_status         = subscription['status']
                sub.save()

                messages.success(self.request, 'Your Subscription downgrade Was Successful!')
                return redirect('users:userPage')
            else:
                messages.warning(self.request, 'Your Subscription cannot be downgraded at this time. Please contact support.')
                return render(self.request, 'payments/subscription_detail.html')

class PaymentMethodManageView(View):
    def get(self, *args, **kwargs):

        subscription_qs = payments_models.Subscription.objects.filter(user=self.request.user)
        if subscription_qs.exists():
            subscription = payments_models.Subscription.objects.get(user=self.request.user)

            if subscription.subscription_status == 'incomplete':
                if subscription.payment_status == 'requires_payment_method':
                    return render(self.request, 'payments/update_payment_method.html')
            elif subscription.subscription_status == 'canceled':
                if subscription.payment_status == 'requires_payment_method':
                    return_message = 'Your subscription is %s. No payment management is needed.' % subscription.subscription_status
                    messages.warning(self.request, return_message)
                    return redirect('users:userPage')
        else:
            return_message = 'Your payment method does not need to be updated!'
            messages.warning(self.request, return_message)
            return redirect('users:userPage')

    def post(self, request, *args, **kwargs):
        stripe.api_key = STRIPE_SECRET_KEY
        token = self.request.POST.get('stripeToken')
        customer = self.request.user.merchant_profile.customer_id

        if request.method == 'POST':
            try:
                payment_method_update =  stripe.Customer.modify(
                                                customer,
                                                source=token,
                                            )

                print(payment_method_update)

                success_message = 'Your payment method updated sucessfully. We will attempt to pay your open invoice in the next 24 hours!'
                messages.success(self.request, success_message)
                return redirect('payments:subscription_detail', slug=self.request.user.subscription.slug)

            except stripe.error.CardError as e:
                messages.warning(self.request, '%s' % e)
                return render(self.request, 'payments/update_payment_method.html')


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
