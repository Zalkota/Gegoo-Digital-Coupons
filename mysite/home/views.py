from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Test

from home.forms import ContacForm
# Create your views here.



#class ContactCreateView(LoginRequiredMixin, CreateView):
#    model = Contact
#    form_class = ContactForm
#    fields = '__all__'
