from django.shortcuts import render
from django.db.models import Subquery
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View

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
from portal.models import Offer, Merchant

#mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Customer email import
from django.conf import settings
EMAIL_CUSTOMER = settings.EMAIL_CUSTOMER


#TODO Remove me
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
latitude = 42.637740
longitude = -83.363546
user_location = Point(longitude, latitude, srid=4326)

from django.db.models import Q, Max
import operator

def get_items(request):
    items_qs = Item.objects.all()
    if items_qs.exists():
        return items_qs
    return None


class homeView(View):
    def get(self, *args, **kwargs):

        merchant_nearby = Merchant.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
        #merchant_nearby = Merchant.objects.annotate(distance = Distance("location", user_location)).annotate(offer_title=Subquery(Offer.values('end_date')[:1])).order_by("distance")

        context = {
            'merchant_list': merchant_nearby,
            # 'offer': offer,
        }
        return render(self.request, 'mysite/home_page.html', context)


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

def components(request):
    return render(request, 'components/main.html')
