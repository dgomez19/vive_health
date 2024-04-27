import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '********* SET HERE YOUR SECRET *********'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
	'rest_framework',
	'api_specialist'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_specialist.urls'

WSGI_APPLICATION = 'api_specialist.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'clinic',
        'USER': 'clinic',
        'PASSWORD': 'clinic',
        'HOST': 'clinic-db',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
}

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "xxxx"
EMAIL_HOST_PASSWORD = "xxxx"
EMAIL_USE_TLS = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
