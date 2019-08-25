from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView, DeleteView, UpdateView
from .models import Membership, UserMembership, Subscription, Transaction, Invoice
from portal.models import Course, Lesson
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

#PDF
from xhtml2pdf import pisa
from django.http import HttpResponse, HttpResponseServerError
from django.utils.text import slugify
# from django.template.loader import render_to_string
# from django.shortcuts import render, redirect, get_object_or_404

# ======== Essential Query Functions  ========

def user_subscriptions_view(request):
	user_membership = get_user_membership(request)
	user_subscription = get_user_subscription(request)
	context = {
		'user_membership': user_membership,
		'user_subscription': user_subscription
	}
	return render(request, "memberships/user_subscription.html", context)

def get_user_membership(request):
	user_membership_qs = UserMembership.objects.filter(user=request.user)
	if user_membership_qs.exists():
		return user_membership_qs.first()
	return None

def get_specified_user_membership(user):
	user_membership_qs = UserMembership.objects.filter(user=user)
	if user_membership_qs.exists():
		return user_membership_qs.first()
	return None

def get_user_subscription(request):
	user_subscription_qs = Subscription.objects.filter(
			user_membership=get_user_membership(request))
	if user_subscription_qs.exists():
		user_subscription = user_subscription_qs.first()
		return user_subscription
	return None

def get_selected_membership(request):
	membership_type = request.session['selected_membership_type']
	selected_membership_qs = Membership.objects.filter(
				membership_type=membership_type)
	if selected_membership_qs.exists():
		return selected_membership_qs.first()
	return None

def get_selected_invoice(request):
	invoice_id = request.session['selected_invoice_id']
	print (invoice_id)
	selected_invoice_qs = Invoice.objects.filter(invoice_id=invoice_id)
	if selected_invoice_qs.exists():
		return selected_invoice_qs.first()
	return None


class MembershipSelectView(ListView):
	model = Membership
	context_object_name = 'membership_list'
	ordering = ['price']
	#Check if user is logged in first

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			current_membership = get_user_membership(self.request)
			context['current_membership'] = str(current_membership.membership)
			return context
		return context

	def post(self, request, **kwargs):
		if request.user.is_authenticated:
			user_membership = get_user_membership(request)
			user_subscription = get_user_subscription(request)

			selected_membership_type = request.POST.get('membership_type') #Obtains the membrship data from form POST

			selected_membership_qs = Membership.objects.filter(
					membership_type=selected_membership_type)
			print(selected_membership_qs)
			selected_membership = selected_membership_qs.first()
			print(selected_membership)
			'''
			==========
			VALIDATION
			==========
			'''
			if user_membership.membership == selected_membership:
				if user_subscription != None:
					messages.info(request, "You already have this membership. Your \
						next payment is due {}".format('get this value from stripe'))
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

			# assign to the session
			request.session['selected_membership_type'] = selected_membership.membership_type

			return HttpResponseRedirect(reverse('memberships:payment'))


@login_required
def InvoicePaymentView(request):

	#Query Essentials
	selected_invoice = get_selected_invoice(request)
	user = request.user
	cus_stripe_id = user.user_stripe.stripe_id
	email = user.email

	#Stripe Key
	publishKey = settings.STRIPE_PUBLISHABLE_KEY

	if request.method == 'POST':
		token = request.POST['stripeToken']
		# Token is created using Checkout or Elements!
		# Get the payment token ID submitted by the form:
		try:
			#customer = stripe.Customer.retrieve(customer_id)  # Creditcard info is linked with customer
			#customer.sources.create(source=token)
            #Modify the customer and add the token from the front end
			stripe.Customer.modify(
			  cus_stripe_id, # cus_xxxyyyyz
			  source=token # tok_xxxx or src_xxxyyy
			)
			charge = stripe.Charge.create(
			amount=selected_invoice.stripe_total,
			currency='usd',
			description='Invoice Charge',
			#source=token
			customer = cus_stripe_id
			#receipt_email= email,
			)

			return redirect(reverse('memberships:update_transactions_invoice',
			kwargs={
				'transaction_info': selected_invoice.invoice_id
			}))
		except stripe.error.CardError as e:
			messages.info(request, "Your card has been declined")
	context = {
	'publishKey': publishKey,
	'invoice': selected_invoice
	}

	return render(request, "memberships/invoice_payment.html", context)

@login_required()
def updateTransactionRecordsInvoice(request, transaction_info):

	selected_invoice = get_selected_invoice(request)
	date_now = datetime.now()

	selected_invoice.payed = True
	selected_invoice.save()

	# Grab User
	#user_profile = get_object_or_404(Profile, user=request.user)

	# Create a transaction
	transaction = Transaction(user=request.user,
							subscription=None,
							invoice_id=transaction_info,
							amount=selected_invoice.amount,
							tax=selected_invoice.tax,
							success=True,
							timestamp=date_now)
	# save the transcation (otherwise doesn't exist)
	transaction.save()

	try:
		del request.session['selected_invoice_id']
	except:
		pass

	#messages.success(request, 'Successfully purchased {} membership'.format(selected_membership))
	messages.success(request, "Payment Received")
	return redirect(reverse('userPage'))


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


def download_invoice_pdf(request, invoice_id):
	#Obtain Object Invoice
	invoice = get_object_or_404(Invoice, pk=invoice_id)

	response = HttpResponse(content_type="application/pdf")
	response["Content-Disposition"] = \
		'%s''%s''%s' % ('filename=', slugify(invoice, True), ".pdf")

	html = render_to_string("memberships/pdf/invoice_pdf.html", {"invoice": invoice})
	status = pisa.CreatePDF(html,
							dest=response,
							link_callback=link_callback)
	if status.err:
		response = HttpReponseServerError("The PDF could not be generated.")
	return response


@login_required
def PaymentView(request):

	user_membership = get_user_membership(request)
	selected_membership = get_selected_membership(request)
	cus_stripe_id = user_membership.user.user_stripe.stripe_id
	publishKey = settings.STRIPE_PUBLISHABLE_KEY

	#totalCost = selected_membership.objects.filter('membership').values('total').annotate(amount=Sum('id', field="price * tax"))
	course_list = Course.objects.filter(membership_required=True).order_by('ordering_id')[:4]

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
	user_membership = get_user_membership(request)
	selected_membership = get_selected_membership(request)

	user_membership.membership = selected_membership
	user_membership.save()

	sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
	sub.stripe_subscription_id = subscription_id
	sub.active = True
	sub.save()

	# Check stripe transaction status TODO
	# This will be part of Webhooks TODO

	# Grab User
	#user_profile = get_object_or_404(Profile, user=request.user)
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
	order_id = str(transaction.order_id)
	price = str(selected_membership.price)
	# Create array
	array = {}
	# Add desired object attritbutes to array
	array['timestamp'] = timestamp
	array['order_id'] = order_id
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

	messages.success(request, 'Successfully purchased {} membership'.format(selected_membership))
	return redirect(reverse('memberships:purchase_success'))


# Success page if transaction was successful
@login_required()
def success(request):

	# Request transaction from stored session
	transaction = request.session.get('transaction', None)
	# Obtain timestamp from JSON string
	timestamp = transaction["timestamp"]
	# Parse string after 10 characters
	data = (timestamp[:10]) if len(timestamp) > 10 else timestamp
	data2 = datetime.strptime(data, '%Y-%m-%d').date()
	# Obtain users new membership #TODO THIS IS AN ISSUE
	user_membership = get_user_membership(request)
	#user = request.user
	#emailRecipient = user.email
	#send_payment_success_email(emailRecipient, user)

	context = {
	'user_membership': user_membership,
	'transaction': transaction,
	'timestamp': timestamp,
	}
	return render(request, 'memberships/purchase_success.html', context)



#Allows user to cancel their own subscription
@login_required
def cancelSubscription(request):
	user_sub = get_user_subscription(request)

	if user_sub.active == False:
	#	messages.info(request, "You dont have an active membership")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
	sub.delete()

	#Set subscription to inactive
	user_sub.active = False
	user_sub.save()

	#Obtain membership of User
	user_membership = get_user_membership(request)

	#Sets users membership to "None"
	user_membership.membership = None
	user_membership.save()

	# Send cancellation email
	emailRecipient = user_membership.user.email
	user = user_membership.user
	send_subscription_cancelation_email(emailRecipient, user)

	messages.success(request, "Membership cancelled")
	# sending an email here

	return redirect('userPage')

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


# ADMIN Panel
class SubscriptionListView(views.SuperuserRequiredMixin, ListView):
	model = Subscription
	context_object_name = 'transaction'  # Default: object_list
	paginate_by = 25
	#queryset = Transaction.objects.all()  # Default: Model.objects.all()
	template_name = 'memberships/subscription_list.html'

	#Superuser Mixin
	login_url = settings.LOGIN_URL
	raise_exception = False
	redirect_field_name = '/'
	redirect_unauthenticated_users = True

class SubscriptionDetailView(views.SuperuserRequiredMixin, DetailView):
	model = Subscription

	slug_field = 'id'
	slug_url_kwarg = 'id'

	#Superuser Mixin
	login_url = settings.LOGIN_URL
	raise_exception = False
	redirect_field_name = '/'
	redirect_unauthenticated_users = True


class TransactionListView(views.SuperuserRequiredMixin, ListView):
	model = Transaction
	context_object_name = 'transaction'  # Default: object_list
	paginate_by = 25
	queryset = Transaction.objects.all()  # Default: Model.objects.all()
	template_name = 'memberships/transaction_list.html'

	#Superuser Mixin
	login_url = settings.LOGIN_URL
	raise_exception = False
	redirect_field_name = '/'
	redirect_unauthenticated_users = True


class TransactionDetailView(views.SuperuserRequiredMixin, DetailView):
	model = Transaction
	slug_field = 'order_id'
	slug_url_kwarg = 'order_id'

	#Superuser Mixin
	login_url = settings.LOGIN_URL
	raise_exception = False
	redirect_field_name = '/'
	redirect_unauthenticated_users = True


	def post(self, request, **kwargs):



		selected_contact_name = request.POST.get('contact_name')
		request.session['selected_contact_name'] = selected_contact_name # Storing data in session

		selected_contact_email = request.POST.get('contact_email')
		request.session['selected_contact_email'] = selected_contact_email # Storing data in session

		return HttpResponseRedirect(reverse('portal:contact_form'))


class MembershipListView(views.SuperuserRequiredMixin, ListView):
	model = Membership
	#queryset = Transaction.objects.all()  # Default: Model.objects.all()
	template_name = 'memberships/membership_panel.html'

	#Superuser Mixin
	login_url = settings.LOGIN_URL
	raise_exception = False
	redirect_field_name = '/'
	redirect_unauthenticated_users = True

def permission_denied(request):
    return render(request, 'memberships/permission_denied.html')

@login_required()
def adminPanel(request):

	#group = Group.objects.get(name='super_user')
	#request.user.groups.add(group)
	if request.user.is_superuser:
	    return render(
	        request,
	        'memberships/admin_panel.html',
	    )

	else:
		return redirect('memberships:permission_denied')





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


# ==================== EMAILS ======================


def send_subscription_cancelation_email(emailRecipient, user):

		subject = 'Mod Technologies Subscription Cancellation Notice'
		sender = 'hello@modwebservices.com'
		receiver = emailRecipient
		context = ({'email': emailRecipient, 'user': user})
		html_content = render_to_string('mail/mail_cancellation.html', context)
		message = render_to_string('mail/mail_cancellation.html', context)
		send_mail(subject,
	              message,
	              sender,
	              [receiver],
	              fail_silently=False,
	              html_message=html_content)

def send_payment_refund_email(emailRecipient, user, selected_amount):
	if not settings.DEBUG:
		subject = 'Mod Technologies Subscription Notice'
		sender = 'hello@modwebservices.com'
		receiver = emailRecipient
		context = ({'email': emailRecipient, 'user': user})
		html_content = render_to_string('mail/mail_success.html', context)
		message = render_to_string('mail/mail_success.html', context)
		send_mail(subject,
	              message,
	              sender,
	              [receiver],
	              fail_silently=False,
	              html_message=html_content)

def send_payment_success_email(emailRecipient, user):

	subject = 'Mod Technologies Subscription Notice'
	sender = 'hello@modwebservices.com'
	receiver = emailRecipient
	context = ({'email': emailRecipient, 'user': user})
	html_content = render_to_string('mail/mail_success.html', context)
	message = render_to_string('mail/mail_success.html', context)
	send_mail(subject,
              message,
              sender,
              [receiver],
              fail_silently=False,
              html_message=html_content)
