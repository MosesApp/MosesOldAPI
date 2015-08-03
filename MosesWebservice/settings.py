"""
Django settings for MosesWebservice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import socket
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

GROUP_STATUS = (('active', 'Active'), ('inactive', 'Inactive'))
PAYMENT_STATUS = (('paid', 'Paid'), ('not paid', 'Not paid'))
BILL_RELATION = (('debtor', 'debtor'), ('taker', 'taker'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ooa+$k1jrw-yvgoaf0+mcvj+a49oxvg72j99=ehmqako5^a^he'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MosesWebserviceApp',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'MosesWebservice.urls'

WSGI_APPLICATION = 'MosesWebservice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'moses',
        'USER': 'moses_user',
        'PASSWORD': 'Moses765',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\', '/'),)

# Absolute filesystem path to the location of the project
# Example: "/var/www/example.com/media/"
PROJECT_ROOT = str(os.getcwd())

STATICFILES_DIRS = (
    (PROJECT_ROOT + os.sep + 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

PRODUCTION = False

IMAGE_FOLDER = 'media' + os.sep + 'images'

if PRODUCTION:
    SERVER_URL = 'http://mosesapp.me/'
    NGINX_PORT = '8000'
    NGINX_SERVER_URL = 'http://mosesapp.me:' + NGINX_PORT
    PROJECT_ROOT = '/home/admin/Moses-Webservice'

else:
    SERVER_URL = 'http://' + str(socket.gethostbyname(socket.gethostname())) +':8000/'
    NGINX_SERVER_URL = ''

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = (PROJECT_ROOT + os.sep + IMAGE_FOLDER + os.sep)

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = NGINX_SERVER_URL + '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = NGINX_SERVER_URL + os.sep + 'media' + os.sep

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'MosesWebserviceApp.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 1000000
}
