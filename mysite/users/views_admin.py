# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Sum

import datetime
import decimal
## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from portal import models as portal_models
from users import models as users_models
from files import models as files_models
from django.utils.text import slugify
from django.views.generic.edit import FormView, FormMixin

from users.decorators import user_is_merchant, IsAdminMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from portal import models as portal_models

from payments import models as payment_models

class AdminDashboardView(View, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        store_qs = portal_models.Store.objects.all()
        user_qs = users_models.MerchantProfile.objects.all().exclude(status='APPROVED')

        end_date = datetime.datetime.now()
        start_date = datetime.datetime.now() + datetime.timedelta(-7)
        subscription_qs = payment_models.Subscription.objects.all().filter(created_at__range=[start_date, end_date], subscription_status='active')

        if subscription_qs.exists():
            single_sub = subscription_qs.first()
            plan = payment_models.Plan.objects.get(plan_id=single_sub.plan_id)
            total_list=[]

            for each in subscription_qs:
                subscription_total = each.subscription_quantity * plan.get_total()
                total_list.append(subscription_total)
            
            aggregate_sum_revenue = sum(total_list)

            context = {
                'stores': store_qs,
                'users': user_qs,
                'subscriptions': subscription_qs,
                'aggregate_sum_revenue': aggregate_sum_revenue,
            }
        else:
            context = {
                'stores': store_qs,
                'users': user_qs,
                'subscriptions': subscription_qs,
            }            

        return render(self.request, 'users/admin/admin_dashboard.html', context)

class AdminApproveUsersView(View, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        user_qs = users_models.MerchantProfile.objects.all()

        context = {
            'users': user_qs,
        }

        return render(self.request, 'users/admin/admin_approve_users.html', context)

class AdminApproveStoresView(View, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        store_qs = portal_models.Store.objects.all()

        context = {
            'stores': store_qs,
        }

        return render(self.request, 'users/admin/admin_dashboard.html', context)

class AdminManageSubscriptionsView(View, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        subscription_qs = payment_models.Subscription.objects.all()

        context = {
            'subscriptions': subscription_qs,
        }

        return render(self.request, 'users/admin/admin_manage_subscriptions.html', context)

class AdminPromotionListView(ListView, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        subscription_qs = payment_models.Subscription.objects.all()

        context = {
            'subscriptions': subscription_qs,
        }

        return render(self.request, 'users/admin/admin_manage_subscriptions.html', context)

class AdminPromotionDetailView(ListView, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        subscription_qs = payment_models.Subscription.objects.all()

        context = {
            'subscriptions': subscription_qs,
        }

        return render(self.request, 'users/admin/admin_manage_subscriptions.html', context)

class AdminPromotionCreateView(ListView, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        subscription_qs = payment_models.Subscription.objects.all()

        context = {
            'subscriptions': subscription_qs,
        }

        return render(self.request, 'users/admin/admin_manage_subscriptions.html', context)

class AdminPromotionDeleteView(ListView, IsAdminMixin):
    def get(self, request, *args, **kwargs):

        subscription_qs = payment_models.Subscription.objects.all()

        context = {
            'subscriptions': subscription_qs,
        }

        return render(self.request, 'users/admin/admin_manage_subscriptions.html', context)