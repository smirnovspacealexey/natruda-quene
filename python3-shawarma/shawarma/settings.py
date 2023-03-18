"""
Django settings for shawarma project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import raven
import psycopg2.extensions

from .my_settings import login, password, db_name, allowed_hosts, debug_flag, listner_url, listner_port, printer_url, \
    raven_dsn, secret_key, server_1c_ip, server_1c_port, getlist_url, server_1c_user, server_1c_pass, order_url, \
    force_to_listner, debug_servery, return_url, carousel_img_dir, carousel_img_url, \
    smtp_server, smtp_port, smtp_login, smtp_password, smtp_from_addr, smtp_to_addr, elastix_action, elastix_login, \
    elastix_script, elastix_secret, elastix_server, delivery_duration, packaging_duration, shashlyk_cooking_duration, \
    shawarma_cooking_duration, dadata_token, LOCAL_TEST

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: keep the secret key used in production secret!
DADATA_TOKEN = dadata_token

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug_flag

DEBUG_SERVERY = debug_servery

ALLOWED_HOSTS = allowed_hosts

# Application definition

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shaw_queue.apps.ShawQueueConfig',
    'apps.main',
    'apps.sms',
    'jquery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shawarma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shawarma.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s \n'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'file_request': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_request.log',
            'formatter': 'verbose'
        },
        'file_server': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_server.log',
            'formatter': 'verbose'
        },
        'file_template': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_template.log',
            'formatter': 'verbose'
        },
        'file_db': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_db.log',
            'formatter': 'verbose'
        },
        '1c': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log/1c.log',
            'formatter': 'verbose'
        },
        'debug_logger': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_logger.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file_request'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_server'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_template'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file_db'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'debug_logger': {
            'handlers': ['debug_logger'],
            'level': 'INFO',
        },
        '1c': {
            'handlers': ['1c'],
            'level': 'INFO',
        },
    },
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': login,
        'PASSWORD': password,
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LISTNER_URL = listner_url

LISTNER_PORT = listner_port

SERVER_1C_IP = server_1c_ip

SERVER_1C_PORT = server_1c_port

GETLIST_URL = getlist_url

ORDER_URL = order_url

RETURN_URL = return_url

PRINTER_URL = printer_url

SERVER_1C_USER = server_1c_user

SERVER_1C_PASS = server_1c_pass

DELIVERY_DURATION = delivery_duration

PACKAGING_DURATION = packaging_duration

SHAWARMA_COOKING_DURATION = shawarma_cooking_duration

SHASHLYK_COOKING_DURATION = shashlyk_cooking_duration

EMAIL_HOST = smtp_server
EMAIL_PORT = smtp_port
EMAIL_USE_TLS = True
SMTP_LOGIN = smtp_login
SMTP_PASSWORD = smtp_password
SMTP_FROM_ADDR = smtp_from_addr
SMTP_TO_ADDR = smtp_to_addr

ELASTIX_SERVER = elastix_server
ELASTIX_SCRIPT = elastix_script
ELASTIX_LOGIN = elastix_login
ELASTIX_SECRET = elastix_secret
ELASTIX_ACTION = elastix_action

CAROUSEL_IMG_DIR = carousel_img_dir

CAROUSEL_IMG_URL = carousel_img_url

FORCE_TO_LISTNER = force_to_listner

LOGIN_REDIRECT_URL = '/shaw_queue/'

STATIC_ROOT = '/home/admintrud/shawarma3/static_content/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

RAVEN_CONFIG = {
    'dsn': raven_dsn,
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

HOST = 'http://shawarma.natruda'


try:
    LOCAL_TEST
except:
    LOCAL_TEST = False

