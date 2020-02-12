# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ry+vd%uy1j2q6z6i3*%x2df_*%7y*!e1x%r-7()5&rmqt*_y#0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'app',

    'airplane',
)

ROOT_URLCONF = 'sample_site.urls'

WSGI_APPLICATION = 'sample_site.wsgi.application'

TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[ os.path.join(BASE_DIR, 'templates'), ],
    'APP_DIRS':True,
}]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

import airplane

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
#    os.path.join(BASE_DIR, airplane.CACHE_DIR),
    airplane.cache_path(),
)

#AIRPLANE_MODE = airplane.BUILD_CACHE
#AIRPLANE_MODE = airplane.USE_CACHE
AIRPLANE_MODE = airplane.AUTO_CACHE
