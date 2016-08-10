## This is the deployment setting for Staging which uses a different database
## than local.

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_secret("RDS_DB_NAME"),
        'USER': get_secret("RDS_DB_USERNAME"),
        'PASSWORD': get_secret("RDS_DB_PASSWORD"),
        'HOST': "postgis",
        "PORT": 5432,
    }
}

# Additional AWS setup
AWS_STORAGE_BUCKET_NAME = get_secret("BUCKET_NAME")
AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
# This will tell boto that when it uploads files to S3, it should set
# properties on them so that when S3 serves them, it'll include those
# HTTP headers in the response. Those HTTP headers in turn will tell
# browsers that they can cache these files for a very long time. It
# makes the browser to load faster.
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


# This is used by the `static` template tag from `static`, if you're
# using that. Or if anything else refers directly to STATIC_URL. So
# it's safest to always set it.
STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'custom_storages.StaticStorage'