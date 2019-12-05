from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
import datetime
from django.utils import timezone
from portal.models import Address
#from shoppingcart.views import get_user_address_default, get_user_orders

#Profile Image
# from .forms import ProfileImageForm
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist




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
