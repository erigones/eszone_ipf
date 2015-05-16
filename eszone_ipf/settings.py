"""
Django settings for eszone_haproxy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# DEVELOPMENT (DEFAULT) SETTINGS
# Secret key for development use only !
SECRET_KEY = '%qlxd*cw(eftb8-w1bxlv^0_rj%am)@u3#$s6ez&^&_#=iaa9i'

# Enable debug for development
DEBUG = True

ALLOWED_HOSTS = []


# PRODUCTION SETTINGS
# You should run this application with ENV=production set in your production environment
if os.environ.get('ENV') == 'production':
    # Provide your secure secret key
    SECRET_KEY = 'write your secret code here'

    # Running with DEBUG enabled in production is insecure
    DEBUG = False

    # Add hosts, which will connect to this API
    ALLOWED_HOSTS = [
        '10.10.10.10',
    ]


# GENERAL SETTINGS
# Definition of used applications
INSTALLED_APPS = (
    'rest_framework',
    'api_ipf',
)

# Definition of used middleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Path within application to main file with url setup
ROOT_URLCONF = 'eszone_ipf.urls'

# Path to file containing wsgi configuration ready for deployment
WSGI_APPLICATION = 'eszone_ipf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# API Version, used also within urls
API_VERSION_PREFIX = 'v1'
