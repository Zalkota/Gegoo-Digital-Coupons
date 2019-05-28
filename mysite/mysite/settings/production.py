from .base import *
from django.core.mail import send_mail

DEBUG = False

# SECURITY ---------------------------------------------------------------------

import os
SECRET_KEY = os.environ["DJANGO_SECRET_KEY_MOD"]

ALLOWED_HOSTS = ['www.modtechnology.io', 'modtechnology.io', '104.248.6.5', '127.0.0.1', '0.0.0.0']
ADMINS = [('ModTechnology', 'dominic@modwebservices.com')]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Added Recently - Not sure if it will work
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
# This ensures that Django will be able to detect a secure connection
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# EMAIL ------------------------------------------------------------------------
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER ='dominic@modwebservices.com'
EMAIL_HOST_PASSWORD = '$Django28' #TODO This should probably go to a python variable
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Captcha ----------------------------------------------------------------------

''' https://accounts.google.com/displayunlockcaptacha '''
try:
    from .local import *
except ImportError:
    pass

# ReCaptcha https://github.com/praekelt/django-recaptcha
RECAPTCHA_PUBLIC_KEY = '6LdGApgUAAAAADzpwNfGePbYmVrZS-2gCCPQyfs6'
RECAPTCHA_PRIVATE_KEY = '6LdGApgUAAAAAJWHqK6Sp7KMPjdq_BpI9NXsxKKc'

RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}

#LIVE #TODO THIS NEED TO GO INTO ENVIRONEMNT VARIABLES ASAP
STRIPE_PUBLISHABLE_KEY = 'pk_live_MdjBMj7pTrz0Dh9XN4wAtlSH'
STRIPE_SECRET_KEY = 'sk_live_6SBA0vgeQtjnrmdFViw6yutU'
