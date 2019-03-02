from .base import *
from django.core.mail import send_mail

DEBUG = False

# SECURITY ---------------------------------------------------------------------

import os
SECRET_KEY = os.environ["DJANGO_SECRET_KEY_STEMLETICS"]

ALLOWED_HOSTS = ['www.dommazzola.com', 'dommazzola.com']
ADMINS = [('Stemletics', 'hello@modwebservices.com')]

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
EMAIL_HOST_USER ='hello@modwebservices.com'
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
RECAPTCHA_PUBLIC_KEY = '6LfDKI0UAAAAAGPojMtiBI1wD-2CYTRFKX765uj4'
RECAPTCHA_PRIVATE_KEY = '6LfDKI0UAAAAADzjHFL5GEL4JTQjL-ZkkJSBu7q6'

RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}
