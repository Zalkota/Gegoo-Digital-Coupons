from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#^57b45ap)gvbl@#@f5v1uqbv)1x3na2ct@xe$ql^r_ds#g0ap'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER ='hello@modwebservices.com'
EMAIL_HOST_PASSWORD = '$Django28' #TODO This should probably go to a python variable
EMAIL_PORT = 587
EMAIL_USE_TLS = True
try:
    from .local import *
except ImportError:
    pass

# ReCaptcha https://github.com/praekelt/django-recaptcha
RECAPTCHA_PUBLIC_KEY = '6LfDKI0UAAAAAGPojMtiBI1wD-2CYTRFKX765uj4'
RECAPTCHA_PRIVATE_KEY = '6LfDKI0UAAAAADzjHFL5GEL4JTQjL-ZkkJSBu7q6'
