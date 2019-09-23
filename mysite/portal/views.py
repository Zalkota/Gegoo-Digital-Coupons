from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView, DeleteView, UpdateView
from django.views import generic, View

#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Email
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

#Models
from .models import Job, Review, Image, Transaction
from users.models import User, Profile

#Forms
from django.views.generic.edit import FormView
from .forms import JobForm, ImageForm

#Login
from django.contrib.auth.decorators import login_required  # This is to block pages to non users using function views
from django.contrib.auth.mixins import LoginRequiredMixin

#Image Uploader
from django.http import JsonResponse

from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils import timezone

#SuperUser Mixin
from braces import views
from django.conf import settings

#appointmentform
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

#Payment
import stripe

def get_selected_job(request):
	job_id = request.session['selected_job_id']
	print (job_id)
	selected_job_qs = Job.objects.filter(id=job_id)
	if selected_job_qs.exists():
		return selected_job_qs.first()
	return None

def get_user_jobs(request):
    user_job_qs = Job.objects.filter(
        user=request.user)
    if user_job_qs.exists():
        user_jobs = user_job_qs.all()
        return user_jobs
    return None


class ImageUploadView(View, LoginRequiredMixin):
	def get(self, request):
		selected_job = get_selected_job(request)
		image_list = Image.objects.filter(job=selected_job)
		return render(self.request, 'portal/image_form_create.html', {'images': image_list})

	def post(self, request):
		form = ImageForm(self.request.POST, self.request.FILES)
		selected_job = get_selected_job(request)
		if form.is_valid():
			image = form.save(commit=False)
			image.job = selected_job
			image = form.save()

			print("save image")
			data = {'is_valid': True, 'name': image.file.name, 'url': image.file.url}
		else:
			print("ELSE")
			data = {'is_valid': False}
		return JsonResponse(data)



class JobListView(ListView, LoginRequiredMixin):
	model = Job



class JobDetailView(DetailView, LoginRequiredMixin):
	model = Job


@login_required
def JobCreateView(request):
	#response.delete_cookie('selected_job_id')
	#reservation = create(Reservation)
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		user = request.user
		form = JobForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			job = form.save(commit=False)
			job.description = form.cleaned_data['description']
			job.desired_plants = form.cleaned_data['desired_plants']
			job.hardscaping = form.cleaned_data['hardscaping']
			job.hardscaping_description = form.cleaned_data['hardscaping_description']
			job.due_date = form.cleaned_data['due_date']
			job.user = user
			print(job.id)
			#reservation.created_time = timezone.now()
			job.save()

			request.session['selected_job_id'] = job.id

			# Add form data to sessions
			#request.session['name'] = reservation.name
			#request.session['time'] = reservation.time
			#request.session['people'] = reservation.people
			#request.session['date'] = reservation.date

			#send_email_reservation(reservation.email, reservation.name, reservation.time, reservation.people)
			#messages.success(request, "Reservation Created")
			#request.session['reservationDate'] = form.cleaned_data['date']
			return redirect('portal:image_upload')

		# If this is a GET (or any other method) create the default form.
	else:
		form = JobForm()
	return render(request, 'portal/job_form_create.html', {'form': form})




class JobUpdateView(SuccessMessageMixin, views.SuperuserRequiredMixin, UpdateView):
    model = Job
    fields = '__all__'
    success_message = "Job Edited Successfully"
    success_url = reverse_lazy('memberships:Job_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True



class JobDeleteView(SuccessMessageMixin, views.SuperuserRequiredMixin, DeleteView):
    model = Job
    warning_message = "Job Deleted"
    success_url = reverse_lazy('memberships:Job_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True


@login_required
def HowItWorks(request):
    return render(request, 'portal/how_it_works.html',)


@login_required
def Review(request, Job):
    form_class = ReviewForm
    review_user = request.user
    if request.method == "GET":
        form_class = ReviewForm(initial={'review_Job': Job, 'review_user': review_user})

    # new logic!
    if request.method == 'POST':
        #form_class = ContactForm(initial={'contact_email': email, 'contact_name': user})
        form = ReviewForm(request.POST)

        if form.is_valid():

            review_Job = request.POST.get(
                'review_Job'
            , '')

            review_summary = request.POST.get('summary', '')

            rating = request.POST.get(
                'rating'
            , '')


            Job_instance = get_Job(Job)

            review = form.save(commit=False)
            review.review_user = review_user
            review.review_Job = Job_instance
            review.summary = review_summary
            review.rating = rating
            review.created_time = timezone.now()
            review.save()
            print ("saved")
            messages.success(request, "Thank you for your review!")
            return redirect('portal:Job_detail', slug=Job_instance.slug)
            #return redirect('portal:Job_list')

    else:
            form = ReviewForm()

    return render(request, 'portal/review_form_create.html', {
        'form': form_class,
    })


@login_required
def JobPaymentView(request):

	selected_job = get_selected_job(request)

	#Query Essentials
	user = request.user
	cus_stripe_id = user.user_stripe.stripe_id
	email = user.email

	print(selected_job.job_image.first())

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
			amount=29900,
			currency='usd',
			description='Payment for 3D Modeling creation of Landscaping',
			#source=token
			customer = cus_stripe_id
			#receipt_email= email,
			)

			return redirect(reverse('portal:update_transaction_job',
			kwargs={
			'transaction_info': selected_job.id
			}))
		except stripe.error.CardError as e:
			messages.info(request, "Your card has been declined")

	context = {
		'publishKey': publishKey,
		'selected_job': selected_job
		}
	return render(request, "portal/job_payment.html", context)



@login_required()
def updateTransactionRecordsJob(request, transaction_info):

	selected_job = get_selected_job(request)
	date_now = timezone.now()

	selected_job.status = "IN PROGRESS"
	selected_job.save()

	# Grab User
	#user_profile = get_object_or_404(Profile, user=request.user)

	# Create a transaction
	transaction = Transaction(user=request.user,
							job=selected_job,
							amount=299,
							success=True,
							timestamp=date_now)
	# save the transcation (otherwise doesn't exist)
	transaction.save()

	try:
		del request.session['selected_job_id']
	except:
		pass

	#messages.success(request, 'Successfully purchased {} membership'.format(selected_membership))
	messages.success(request, "Payment Received")
	return redirect(reverse('userPage'))


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
	#'user_membership': user_membership,

	}
	return render(request, 'memberships/purchase_success.html', context)
