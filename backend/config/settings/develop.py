from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['*']
SITE_URL = "http://127.0.0.1:8080/"
MEDIA_URL = '/media/'
STATIC_URL = 'public/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smartdoctor',
        'USER': 'smartdoctor',
        'PASSWORD': 'smartdoctor',
        'HOST': 'dev-smartdoctor-db',
        'PORT': '5432',
    }
}

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (  # noqa: F405
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer'
)
