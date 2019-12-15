from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
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

class userPage(View):
    def get(self, *args, **kwargs):
        try:
            user = self.request.user

            context = {
                    'user': user,
            }
            return render(self.request, "users/userPage.html", context)

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

            city_qs = City.objects.filter(name=city)
            city = city_qs.first()

            state_qs = Region.objects.filter(name=state)
            state = state_qs.first()
            print(state)

            # edit the order

            user = self.request.user



            # store the object
            user_address = user.user_profile.address
            user_address.state = state
            user_address.city = city
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
