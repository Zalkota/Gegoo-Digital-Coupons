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

#TEST
STRIPE_PUBLISHABLE_KEY = 'pk_test_idvhfKDQ341zGBS85RwhLnWY'
STRIPE_SECRET_KEY = 'sk_test_UreA2MI54Bmadk6xO2j9jGlD'



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
