from .base import *
from django.core.mail import send_mail

DEBUG = False

# SECURITY ---------------------------------------------------------------------

import os

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1').split(',')

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



#LIVE #TODO THIS NEED TO GO INTO ENVIRONEMNT VARIABLES ASAP
STRIPE_PUBLISHABLE_KEY = 'pk_live_MdjBMj7pTrz0Dh9XN4wAtlSH'
STRIPE_SECRET_KEY = 'sk_live_6SBA0vgeQtjnrmdFViw6yutU'



# S3 ------------------------------------------------------------------------
import datetime
AWS_ACCESS_KEY_ID = "AKIAXTP3WIX7E34PG34V"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'mysite.settings.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'mysite.settings.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'static-gegoo-bucket'
S3DIRECT_REGION = 'us-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

# ELASTIC SEARCH ----------------------------------------------------------
INTERNAL_IPS = [

    '167.172.255.65',

]
