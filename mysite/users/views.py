from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View, FormView
# from memberships.views import get_user_memberships, get_user_subscriptions #TODO
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from portal.models import Store
from location.models import Address
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
import datetime
from django.utils import timezone
from location.models import Address
from .forms import userLocationForm
from django.contrib import messages
#from shoppingcart.views import get_user_address_default, get_user_orders

#Profile Image
# from .forms import ProfileImageForm
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from cities_light.models import Region, City

from allauth.account.views import SignupView
from users.forms import MerchantSignupForm

from portal import models as portal_models



class userPage(View):
    def get(self, *args, **kwargs):
        try:
            user = self.request.user
            stores = portal_models.Store.objects.filter(merchant=user).order_by('-views')
            offers = portal_models.Offer.objects.filter(author=user)
            current_date = timezone.now
            context = {
                'user': user,
                'stores': stores,
                'offers': offers,
                'current_date': current_date,
            }

            #Render Merchant Page
            if user.is_merchant == True:
                return render(self.request, "users/merchant_profile_mpm.html", context)

            #Render Normal User Profile Page
            elif user.is_merchant == False:
                    return render(self.request, "users/merchant_profile_mpm.html", context)


        except ObjectDoesNotExist:
            messages.info(self.request, "Error contact admin")
            return redirect("home-page")


# class userLocaton(FormView):
#     form_class = userLocationForm
#     template_name = 'users/user_location_form.html'
#     success_url = reverse_lazy('userPage')
#     success_message = "Location Changed!"
#
#     def form_valid(self, form):
#         return super(userLocaton, self).form_valid(form)

# <**************************************************************************>
# <*****                     User Non Merchant Views                    *****>
# <**************************************************************************>

class userLocaton(View):
    def get(self, *args, **kwargs):
        form = userLocationForm()

        user = self.request.user
        address = user.user_profile.address

        context = {
            'form': form,
            'address': address
        }
        return render(self.request, "users/user_location_form.html", context)

    def post(self, *args, **kwargs):
        form = userLocationForm(self.request.POST)
        if form.is_valid():
            #ref_code = self.kwargs['ref_code']
            city = form.cleaned_data.get('city_input')
            state = form.cleaned_data.get('state_input')

            city_qs = City.objects.get(name=city)
            state_qs = Region.objects.get(name=state)


            # edit the order

            user = self.request.user

            # store the object
            user_address = user.user_profile.address
            user_address.state = state_qs
            user_address.city = city_qs
            # user_address.user =
            user_address.save()
            print("saved")

            messages.success(self.request, "Location changed")
            return redirect("users:user_location")



class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class RedirectProfileView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return HttpResponseRedirect(
                    reverse('users:summary',
                            kwargs={'username': self.request.user.username}))


# <**************************************************************************>
# <*****                     User Merchant Views                        *****>
# <**************************************************************************>


# class MerchantStoreListView(LoginRequiredMixin, ListView): #TODO this should only be viewable by merchants
#     # model = Merchant
#     # template_name = 'users/user_merchant_store_list.html'

#     # def get_queryset(self):
#     #     return Merchant.objects.filter(user=self.request.user)


class MerchantSignUpView(SignupView):

    template_name = 'account/signup_merchant.html'
    form_class = MerchantSignupForm
    view_name = 'merchant-signup'
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        ret = super(MerchantSignUpView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


# class MerchantSubscriptionsView(LoginRequiredMixin, View):
#     def get(self):
#         # user_membership_list = get_user_memberships(request)
#         # user_subscription_list = get_user_subscriptions(request)
#         context = {
#             'user_membership_list': user_membership_list,
#             'user_subscription_list': user_subscription_list
#         }
#         return render(request, "users/user_merchant_subscription.html", context)

# class ConsumerSignUpView(SignupView):
#
#     template_name = 'account/consumer_signup.html'
#     form_class = ConsumerSignupForm
#     view_name = 'consumer-signup'
#     success_url = '/'
#
#     def get_context_data(self, **kwargs):
#         ret = super(ConsumerSignUpView, self).get_context_data(**kwargs)
#         ret.update(self.kwargs)
#         return ret
