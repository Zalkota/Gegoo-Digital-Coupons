from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Profile
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from memberships.models import Membership, UserMembership, Subscription, Invoice
from memberships.views import get_user_membership, get_user_subscription

#Profile Image
from .forms import ProfileImageForm
from django.shortcuts import get_object_or_404

#wagtail



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

@login_required
def userPage(request):
    model = User
    user = request.user


    if request.method == 'POST':
        selected_invoice_id = request.POST.get('invoice_id') #Obtains the membrship data from form POST
        selected_invoice_qs = Invoice.objects.filter(
        invoice_id=selected_invoice_id)
        print('selected_invoice_qs', selected_invoice_qs)
        selected_invoice = selected_invoice_qs.first()
        print('selected_invoice',selected_invoice)
        # assign to the session
        request.session['selected_invoice_id'] = selected_invoice.invoice_id
        return HttpResponseRedirect(reverse('memberships:invoice_payment'))

    if user.user_membership != None: #BROKEN

        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        print(user_membership, user_subscription)

        context = {
                'user': user,
        		'user_membership': user_membership,
        		'user_subscription': user_subscription
                }
        template = 'users/userPage.html'
        return render(request, template, context)

    context = {
            'user': user,
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


def user_subscriptions_view(request):
	user_membership = get_user_membership(request)
	user_subscription = get_user_subscription(request)
	context = {
		'user_membership': user_membership,
		'user_subscription': user_subscription
	}
	return render(request, "users/user_subscription.html", context)


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
