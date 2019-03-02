from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse
from django.urls import reverse, reverse_lazy

def security(request):
    return render(request, 'security.txt')
