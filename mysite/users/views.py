from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
import datetime
from django.utils import timezone
from shoppingcart.models import Address
from shoppingcart.views import get_user_address_default, get_user_orders

#Profile Image
from .forms import ProfileImageForm
from django.shortcuts import get_object_or_404


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

@login_required
def userPage(request):
    model = User
    user = request.user
    address = get_user_address_default(request, user)
    orders = get_user_orders(request, user)

    print(address)


    context = {
            'user': user,
            'address': address,
            'order_list': orders,
            }
    template = 'users/userPage.html'
    return render(request, template, context)

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


def user_jobs_view(request):
	user_jobs = get_user_jobs(request)
	context = {
		'user_jobs': user_jobs
	}
	return render(request, "users/user_jobs.html", context)


#Profile Image
@login_required
def add_image(request):
    user = request.user
    instance, status = Profile.objects.get_or_create(user=user)
    if status:
        instance = Profile.objects.create(user=user)

    form = ProfileImageForm(instance=instance)
    if request.method == "POST":
        form = ProfileImageForm(data=request.POST, files=request.FILES, instance=instance)
    if form.is_valid():
        form = form.save(commit=False)
        #form.user=request.user.pk
        form.save()
        return redirect('userPage')
    else:
        return render(request, "users/user_image_form.html", {"form": form
            })
