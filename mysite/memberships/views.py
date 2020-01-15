from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView, DeleteView, UpdateView, View
from .models import Membership, UserMembership, Subscription, Transaction
from portal.models import Store
from users.models import User
from django.urls import reverse, reverse_lazy
#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
#mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .json import json_serial, DecimalEncoder
import json
from datetime import date, datetime
#SuperUser Mixin
from braces import views

#Payment
import stripe

from .emails import send_subscription_cancelation_email, send_payment_refund_email, send_payment_success_email

#Random Number generator
import random
import string



# def random_string_generator(size=10, chars=string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))
#

# def unique_order_id_generator():
#     new_ref_code= random_string_generator()
#
#     qs_exists= Order.objects.filter(ref_code=new_ref_code).exists()
#     if qs_exists:
#         return unique_order_id_generator(instance)
#     return new_ref_code

# ======== Essential Query Functions  ========



def get_user_membership(request):
    try:
        user_membership_qs = UserMembership.objects.get(user=request.user)
        if user_membership_qs:
            return user_membership_qs
        return None
    except:
        pass


def get_specified_user_membership(user):
	user_membership_qs = UserMembership.objects.get(user=user)
	if user_membership_qs:
		return user_membership_qs
	return None

def get_user_subscriptions(request):
    user_subscription_qs = Subscription.objects.filter(
    user=request.user)
    if user_subscription_qs.exists():
        user_subscription_list = user_subscription_qs
        return user_subscription_list
    return None


def get_selected_membership(request):
	membership_type = request.session['selected_membership_type']
	selected_membership_qs = Membership.objects.get(
				membership_type=membership_type)
	if selected_membership_qs:
		return selected_membership_qs
	return None


class MembershipSelectView(ListView):
	model = Membership
	context_object_name = 'membership_list'
	ordering = ['price']
	#Check if user is logged in first


	def post(self, request, **kwargs):
		if request.user.is_authenticated:
			user_membership = get_user_membership(request)
			user_subscriptions = get_user_subscriptions(request)

			selected_membership_type = request.POST.get('membership_type') #Obtains the membrship data from form POST

			selected_membership_qs = Membership.objects.get(
					membership_type=selected_membership_type)
			print(selected_membership_qs)
			selected_membership = selected_membership_qs
			print(selected_membership)
			'''
			==========
			VALIDATION
			==========
			'''
			if user_membership != None:
				if user_membership == selected_membership:
					if membership.user_subscriptions != None:
						messages.info(request, "You already have this membership. Your \
							next payment is due {}".format('get this value from stripe'))
						return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

			# assign to the session
			request.session['selected_membership_type'] = selected_membership.membership_type

			return HttpResponseRedirect(reverse('memberships:payment'))



def link_callback(uri, rel):
	# convert URIs to absolute system paths
	if uri.startswith(settings.MEDIA_ROOT):
		path = os.path.join(settings.MEDIA_ROOT,
							uri.replace(settings.MEDIA_URL, ""))
	elif uri.startswith(settings.STATIC_URL):
		path = os.path.join(settings.STATIC_ROOT,
							uri.replace(settings.STATIC_URL, ""))
	else:
		# handle absoluteuri (ie: http://my.tld/a.png)
		return path

	# make sure that the file exists
	if not os.path.isfile(path):
		raise Exception(
			"Media URI must start with "
			'%s' % (settings.STATIC_URL or settings.MEDIA_URL))
	return path


@login_required
def PaymentView(request):

	user_membership = get_user_membership(request)
	selected_membership = get_selected_membership(request)
	user_subscription_list = get_user_subscriptions(request)

	if user_subscription_list != None:
		for subscription in user_subscription_list:
			if subscription.active != False:
				active_membership = subscription.user_membership.membership
				if selected_membership == active_membership:
					print('error')
					messages.info(request, "You already have this membership")
					return redirect(reverse('memberships:select'))

	cus_stripe_id = request.user.merchant_profile.stripe_id #TODO Create Stripe ID at this point
	publishKey = settings.STRIPE_PUBLISHABLE_KEY


	if request.method == "POST":
		try:
			token = request.POST['stripeToken']

            #Modify the customer and add the token from the front end
			stripe.Customer.modify(
			  cus_stripe_id, # cus_xxxyyyyz
			  source=token # tok_xxxx or src_xxxyyy
			)
			#customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
			#customer.source = token # 4242424242424242
			#customer.save()

            #Now we can create the subscription using only the customer as we don't need to pass their credit card source anymore
			subscription = stripe.Subscription.create(
			  customer=cus_stripe_id,
			  items=[
			    {
			      "plan": selected_membership.stripe_plan_id,
			    },
			  ],
			)
			return redirect(reverse('memberships:update_transactions',
				kwargs={
					'subscription_id': subscription.id
				}))

		except stripe.error.CardError as e:
			messages.info(request, "Oops, your card has been declined")

	context = {
	'publishKey': publishKey,
	'selected_membership': selected_membership
	}

	return render(request, "memberships/membership_payment.html", context)


@login_required()
def updateTransactionRecords(request, subscription_id):
    user = request.user
    selected_membership = get_selected_membership(request)
    print('test', selected_membership)

    membership, created = UserMembership.objects.get_or_create(user=user)
    membership.membership = selected_membership
    membership.save()

    sub, created = Subscription.objects.get_or_create(user_membership=membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.user = user
    sub.save()


    # create a transaction
    transaction = Transaction(user=request.user,
    subscription=sub,
    amount=selected_membership.price,
    tax=selected_membership.tax,
    success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()

    #Serialize timestamp
    timestamp = json_serial(transaction.timestamp)
    #Turn UUID into a Storing
    sub = str(sub)
    id = str(transaction.id)
    price = str(selected_membership.price)
    # Create array
    array = {}
    # Add desired object attritbutes to array
    array['timestamp'] = timestamp
    array['id'] = id
    array['subscription'] = sub
    array['price'] = price
    # Convert to JSON string
    json.dumps(array, indent=4, sort_keys=True, default=str)
    # Add array to sessions
    request.session['transaction'] = array
    # Remove sessions from other view
    try:
        del request.session['selected_membership_type']
    except:
        pass

    context = {
    'selected_membership': selected_membership
    }
    user = user
    emailRecipient = user.email
    send_payment_success_email(emailRecipient, user)

    messages.success(request, 'Successfully purchased {} membership'.format(selected_membership))
    return redirect(reverse('memberships:purchase_success',
        kwargs={
        'selected_membership': selected_membership
        }))



# Success page if transaction was successful
@login_required()
def success(request, selected_membership):

	# Request transaction from stored session
	transaction = request.session.get('transaction', None)
	# Obtain timestamp from JSON string
	timestamp = transaction["timestamp"]
	# Parse string after 10 characters
	data = (timestamp[:10]) if len(timestamp) > 10 else timestamp
	data2 = datetime.strptime(data, '%Y-%m-%d').date()

	#user = request.user
	#emailRecipient = user.email
	#send_payment_success_email(emailRecipient, user)

	context = {
	'user_membership': selected_membership,
	'transaction': transaction,
	'timestamp': timestamp,
	}
	return render(request, 'memberships/purchase_success.html', context)



#Allows user to cancel their own subscription
@login_required
def cancelSubscription(request, subscription_id):

    user = request.user
    user_subscription_qs = Subscription.objects.filter(id=subscription_id)
    user_sub = user_subscription_qs.first()


    if user_sub.active == False:
        #	messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if user == user_sub.user:
        sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
        sub.delete()

        #Set subscription to inactive
        user_sub.active = False
        user_sub.save()

        #Sets users membership to "None"
        user_membership = user_sub.user_membership.membership

        user_sub.user_membership.membership = None
        user_membership.save()

        # Send cancellation email
        user = user_sub.user
        emailRecipient = user.email
        send_subscription_cancelation_email(emailRecipient, user)

        messages.success(request, "Membership cancelled")
        # sending an email here

    return redirect('user_subscription')

#Allows admin to cancel subscriptions
@login_required
def cancelSubscriptionAdmin(request, stripe_subscription_id, user):
	#user_sub = get_user_subscription(request)
	if request.method == "GET":
		user_sub = stripe_subscription_id

	user_sub_qs = Subscription.objects.filter(
			stripe_subscription_id=user_sub)
	print(user_sub_qs)
	selected_subscription = user_sub_qs.first()
	print(selected_subscription)


	if selected_subscription.active == False:
		messages.warning(request, "Membership not active")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	#Cancels the subscription on stripes side
	sub = stripe.Subscription.retrieve(stripe_subscription_id)
	sub.delete()

	#Set subscription to inactive
	selected_subscription.active = False
	selected_subscription.save()

	#Obtain Free membership objects
	#free_membership = Membership.objects.filter(membership_type='Free').first()

	#Obtain user object
	user = User.objects.filter(username=user).first()

	#Obtain membership of specific user in question.. Not request.user
	user_membership = get_specified_user_membership(user)

	#Sets users membership to "None"
	user_membership.membership = None
	user_membership.save()



	# sending an email here
	emailRecipient = user_membership.user.email
	send_subscription_cancelation_email(emailRecipient, user)

	messages.success(request, "Membership cancelled")

	return redirect('/')


#Disregarding this feature for now
@login_required
def refundSubscriptionAdmin(request, stripe_subscription_id, user):
	if request.method == "GET":
		user_sub = stripe_subscription_id

	#Check that sub is active
	if user_sub.active == False:
		messages.info(request, "You dont have an active membership")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	selected_amount = request.POST.get('amount')
	request.session['selected_amount'] = selected_amount # Storing data in session

	sub = stripe.Subscription.retrieve(stripe_subscription_id)

	publishKey = settings.STRIPE_PUBLISHABLE_KEY

	refund = stripe.Refund.create(
	    charge=sub,
	    amount=selected_amount,
		)

	#Delete stripe subscription
	sub.delete()
	#Set subscription to unactive
	user_sub.active = False
	user_sub.save()

	#Sets users membership to "free"
	free_membership = Membership.objects.filter(membership_type='Free').first()
	user_membership = get_user_membership(request)
	user_membership.membership = null;  #TODO WILL THIS WORK?
	user_membership.save()

	#Send email to user
	emailRecipient = user.email
	send_payment_refund_email(emailRecipient, user, selected_amount)

	#create messagef
	messages.info(request, "Membership refunded. Email sent to the customer")
	# sending an email here

	return redirect('userPage')




class MembershipListView(views.SuperuserRequiredMixin, ListView):
	model = Membership
	ordering = ['position']
	#queryset = Transaction.objects.all()  # Default: Model.objects.all()
	template_name = 'memberships/membership_panel.html'

	#Superuser Mixin
	login_url = settings.LOGIN_URL
	raise_exception = False
	redirect_field_name = '/'
	redirect_unauthenticated_users = True

def permission_denied(request):
    return render(request, 'memberships/permission_denied.html')


class MembershipUpdateView(SuccessMessageMixin, views.SuperuserRequiredMixin, UpdateView):
    model = Membership
    fields = '__all__'
    success_message = "Membership Edited Successfully"
    success_url = reverse_lazy('memberships:admin_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True
