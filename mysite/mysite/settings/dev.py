from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '#^57b45ap)gvbl@#@f5v1uqbv)1x3na2ct@xe$ql^r_ds#g0ap'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER ='dominic@modwebservices.com'
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

#NEILS STRIPE ACCOUNT
STRIPE_PUB_KEY      = 'pk_test_ytOTGb9MgWKRqiFD3jL10LAb00sMmoKS8P'
STRIPE_SECRET_KEY   = 'sk_test_Eu5hX5Y9os8wHLuu09bW8Cz600mtFK7crK'

#MICHAELS STRIPE ACCOUNT Please do not change the variable "Stripe_Secret_Key" it does nothing.
# STRIPE_PUB_KEY      = 'pk_test_k2kLiCPSsK7yyQF4rDDPhHN100mYwH0Pvj'
# STRIPE_SECRET_KEY   = 'sk_test_vZfYk3ISvw6WsynV64vP0XpK006WkTHRMI'


# S3 ------------------------------------------------------------------------
import datetime
AWS_ACCESS_KEY_ID = "AKIAXTP3WIX7E34PG34V"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'mysite.settings.aws.utils.MediaRootS3BotoStorageDev'
# STATICFILES_STORAGE = 'mysite.settings.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'static-gegoo-bucket'
S3DIRECT_REGION = 'us-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media-dev/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
# STATIC_URL = 'static/'
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}


# ELASTIC SEARCH ----------------------------------------------------------
INTERNAL_IPS = [

    '127.0.0.1',

]

HAYSTACK_CONNECTIONS = {
  'default': {
  'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
  'URL': 'http://elasticsearch:9200/',
  'INDEX_NAME': 'products_tutorial',
  },
}
