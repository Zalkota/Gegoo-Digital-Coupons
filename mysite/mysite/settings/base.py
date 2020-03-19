"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
# from mysite.settings.aws.conf import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '#^57b45ap)gvbl@#@f5v1uqbv)1x3na2ct@xe$ql^r_ds#g0ap')
DEBUG = os.getenv('DJANGO_DEBUG', False)

# S3_USE_SIGV4 = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'modelcluster',
    'taggit',
    'mysite',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'debug_toolbar',

    #S3 Upload
    'rest_framework',
    'files',

    #APPS
    'users',
    'portal',
    'support',
    # 'memberships',

    #Payment
    'stripe',
    'payments.apps.PaymentsConfig',
    'django_countries',

    #Security
    'honeypot',

    #Phone Number Field
    'phonenumber_field',

    #PDF
    #'xhtml2pdf',

    #editor
    'ckeditor',
    'ckeditor_uploader',

    #ImportExport
    'import_export',

    #Custom Forms with classes
    #'widget_tweaks',
    'crispy_forms',

    #Search
    'search',
    'haystack',
    #'django_elasticsearch_dsl',

    #GeoDjango
    'location',
    'django.contrib.gis',
    #'leaflet',
    'geolite2',
    #'ipware',
    'cities_light',



    #S3 Static Files
    'storages',

    #ALLAUTH
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    #debug toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]







#honeypot
HONEYPOT_FIELD_NAME = 'phonenumber'

PHONENUMBER_DEFAULT_REGION = 'US'

ROOT_URLCONF = 'mysite.urls'

CKEDITOR_UPLOAD_PATH = "uploads/"

# Form Rendering
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['compressor']
STATICFILES_FINDERS = ['compressor.finders.CompressorFinder']
#TODO: I should probably run the compressor offline then cache the results
#TODO: Minify the JS?
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),  #libsass for scss to CSS
)



from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'mysite.processors.SiteName',
                # 'mysite.processors.PromotionProcessor',
                # 'mysite.processors.AuthenticatedUserLocation',
                # 'mysite.processors.get_client_ip',
                'mysite.processors.classloudFrontURL',
                #'allauth.account.context_processors',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #'allauth.account.context_processors.account',
                #'allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#
# 	'default': {
#         	'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         	'NAME': 'gegoo',
#         	'USER': 'gegooadmin',
#         	'PASSWORD': '$Django10',
#         	'HOST': 'localhost',
#         	'PORT': '',
#     }
# }

DATABASES = {
     'default': {
         'ENGINE': os.getenv('DATABASE_ENGINE', 'django.contrib.gis.db.backends.postgis'),
         'NAME': os.getenv('DATABASE_NAME', 'gegoo'),
         'USER': os.getenv('DATABASE_USERNAME', 'gegooadmin'),
         'PASSWORD': os.getenv('DATABASE_PASSWORD', '$Django10'),
         'HOST': os.getenv('DATABASE_HOST', 'localhost'),
         'PORT': os.getenv('DATABASE_PORT', ''),
         'OPTIONS': json.loads(
             os.getenv('DATABASE_OPTIONS', '{}')
         ),
     }
 }


#GEOIP DATABASE LOCATION
# GEOIP_PATH = '/location/location_db/'
# GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'
# GEOIP_CITY = 'GeoLite2-City.mmdb'

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['US']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
raise_exception = True
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/dashboard/'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash


SITE_ID = 1


# Your stuff...
# ------------------------------------------------------------------------------
# Some really nice defaults

ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
#ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True # By changing this setting to False, logged in users will not be redirected when they access login/signup pages.
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # User can login with username or email
ACCOUNT_USERNAME_REQUIRED = False  # TODO: What about HOS Users??

ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# Determines the expiration date of email confirmation mails (# of days).
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
# In order to verify an email address a key is mailed identifying the email address to be verified. In previous versions, a record was stored in the database for each ongoing email confirmation, keeping track of these keys. Current versions use HMAC based keys that do not require server side state.
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none". When set to “mandatory” the user is blocked from logging in until the email address is verified. Choose “optional” or “none” to allow logins with an unverified e-mail address. In case of “optional”, the e-mail verification mail is still sent, whereas in case of “none” no e-mail verification mails are sent.

# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
# Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none". When set to “mandatory” the user is blocked from logging in until the email address is verified. Choose “optional” or “none” to allow logins with an unverified e-mail address. In case of “optional”, the e-mail verification mail is still sent, whereas in case of “none” no e-mail verification mails are sent.
ACCOUNT_EMAIL_SUBJECT_PREFIX =''
# Subject-line prefix to use for email messages sent. By default, the name of the current Site (django.contrib.sites) is used.
ACCOUNT_DEFAULT_HTTP_PROTOCOL ='http'

# Security
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400

ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_REDIRECT_URL ='/'
ACCOUNT_SIGNUP_FORM_CLASS = None            #Custom Content -> 'users.forms.SignupForm'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD ='email'
ACCOUNT_USER_MODEL_USERNAME_FIELD ='username'

ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # The default behaviour is not log users in and to redirect them to ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
#By changing this setting to True, users will automatically be logged in once they confirm their email address. Note however that this only works when confirming the email address immediately after signing up, assuming users didn’t close their browser or used some sort of private browsing mode.

#ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = 'True'  # Default is false
ACCOUNT_SESSION_REMEMBER = 'None' # Default is None. Controls the life time of the session. Set to None to ask the user 'Remember me?', False to not remember, and True to always remember.
#ACCOUNT_SIGNUP_FORM_CLASS = 'None'  # A string pointing to a custom form class (e.g. ‘myapp.forms.SignupForm’) that is used during signup to ask the user for additional input (e.g. newsletter signup, birth date). This class should implement a def signup(self, request, user) method, where user represents the newly signed up user.
#ACCOUNT_USERNAME_BLACKLIST = []
#ACCOUNT_USERNAME_MIN_LENGTH = 1

#TEST
#STRIPE_PUBLISHABLE_KEY = 'pk_test_idvhfKDQ341zGBS85RwhLnWY'
#STRIPE_SECRET_KEY = 'sk_test_UreA2MI54Bmadk6xO2j9jGlD'

# STRIPE_PUB_KEY_LIVE      = 'pk_test_ytOTGb9MgWKRqiFD3jL10LAb00sMmoKS8P' #NEILS
# STRIPE_SECRET_KEY_LIVE   = 'sk_test_Eu5hX5Y9os8wHLuu09bW8Cz600mtFK7crK' #NEILS

STRIPE_PUB_KEY_TEST      = 'pk_test_k2kLiCPSsK7yyQF4rDDPhHN100mYwH0Pvj'
STRIPE_SECRET_KEY_TEST   = 'sk_test_vZfYk3ISvw6WsynV64vP0XpK006WkTHRMI'


EMAIL_CUSTOMER = 'dominic@modwebservices.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'michael@modwebservices.com'
EMAIL_HOST_PASSWORD = 'Florida1122pc$'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (42.3314, -83.0458),
    'DEFAULT_ZOOM': 5,
    'MAX_ZOOM': 20,
    'MIN_ZOOM': 3,
    'SCALE': 'imperial',
    'ATTRIBUTION_PREFIX': 'MOD Technologies LLC'
}

DATE_INPUT_FORMATS = ['%d/%m/%Y']
