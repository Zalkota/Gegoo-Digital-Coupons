from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Contact Form
from django.views.generic.edit import FormView, FormMixin

# Reservation form
from django.http import HttpResponse
from .forms import ContactForm, ContactMiniForm
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone

# imports
from .models import Contact
from shoppingcart.models import Item

#mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Customer email import
from django.conf import settings
EMAIL_CUSTOMER = settings.EMAIL_CUSTOMER

def get_items(request):
    items_qs = Item.objects.all()
    if items_qs.exists():
        return items_qs
    return None

def home(request):

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ContactMiniForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            contact = form.save(commit=False)
            contact.name = form.cleaned_data['name']
            contact.phone = form.cleaned_data['phone']
            contact.email = form.cleaned_data['email']
            contact.description = form.cleaned_data['description']
            #print( reservation.email)
            contact.save()

            #send_email_reservation(reservation.email)
            #messages.success(request, "Email Subscribed")
            #request.session['reservationDate'] = form.cleaned_data['date']

            return HttpResponseRedirect('/contact_landing_page/')
        # If this is a GET (or any other method) create the default form.
    else:
        form = ContactMiniForm()

    #service_list = get_service(request)

    item_list = get_items(request)


    context = {
    'item_list': item_list,
    }
    return render(request, 'mysite/home_page.html', context)



class ContactFormView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy('contact-landing-page')
    template_name = 'mysite/contact_page.html'


    def form_valid(self, form):

        ContactForm = form.save(commit=False)
        ContactForm.name = form.cleaned_data['name']
        ContactForm.email = form.cleaned_data['email']
        ContactForm.phone = form.cleaned_data['phone']
        ContactForm.company = form.cleaned_data['company']
        ContactForm.description = form.cleaned_data['description']
        ContactForm.save()

        send_email(ContactForm.name, ContactForm.email, ContactForm.phone, ContactForm.company, ContactForm.description)

        #template = get_template('contact_template.txt')
        #context = Context({
        #    'contact_name': contact_name,
        #    'contact_email': contact_email,
        #    'form_content': form_content
        #})
        #content = template.render(context)

        #email = EmailMessage(
        #    'New contact form submission',
        #    content,
        #    'Your website ' + '',
        #    ['youremail@gmail.com'],
        #    headers = {'Reply-To': contact_email}
        #
        #email.send()
        return super(ContactFormView, self).form_valid(form)

def contactLandingPage(request):
    return render(request, 'mysite/form_page_landing.html')

def security(request):
    return render(request, 'security.txt')

<<<<<<< HEAD
def components(request):
    return render(request, 'mysite/components.html')
=======
def componentsMain(request):
    return render(request, 'components/main.html')
>>>>>>> b5842b25006178a515114cd9b1b3849fb06a7f73
