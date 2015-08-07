#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Django settings for CloudHaven project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# AWS_STORAGE_BUCKET_NAME = 'clhavenstaticfiles'
# AWS_ACCESS_KEY_ID = 'AKIAIIHCYMEIDJUP5QDA'
# AWS_SECRET_ACCESS_KEY = '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'
#
#     # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
#     # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
#     # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
#     # We also use it in the next setting.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#
#     # This is used by the `static` template tag from `static`, if you're using that. Or if anything else
#     # refers directly to STATIC_URL. So it's safest to always set it.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
#
#     # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
#     # you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '++zp!v95(ccg(bv)^1o3j-pz&@3tvl0t#df#&4kse*xlwl0lya'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


TEMPLATE_CONTEXT_PROCESSORS = (
    # Put 'django.contrib.auth.context_processors.auth' in
    # your TEMPLATE_CONTEXT_PROCESSORS setting in order to use the admin application.
    "django.contrib.auth.context_processors.auth",

    "account.context_processors.account",
    "home.context_processors.user_dropbox_connection",
    "home.context_processors.user_google_connection",
    "home.context_processors.user_box_connection",
    "home.context_processors.user_files_uploaded",
    "home.context_processors.user_file_upload_form",

)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Trying django-user-accounts
    'account',
    'django_forms_bootstrap',
    'bootstrap3',
    'storages',
    'home',
    'filehandler',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # django-user-accounts
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
)

ROOT_URLCONF = 'cloudhaven.urls'
WSGI_APPLICATION = 'cloudhaven.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        # 'HOST': '/cloudsql/silver-retina-86821:cloudhaven',
#        'NAME': 'cloudhaven_dev',
#        'USER': 'root',
#        'PASSWORD': 'root',
#    }
#}

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'df53fb3a747cb43e7b50386d453df4ba7',
            'USER': 'u3fZzmLPT3K9T',
            'PASSWORD': 'p3A7wqhds4l76',
            'HOST': '192.155.247.247',
            'PORT': '3307',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

ACCOUNT_LOGIN_REDIRECT_URL = '/home'

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False

# For file uploads
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
