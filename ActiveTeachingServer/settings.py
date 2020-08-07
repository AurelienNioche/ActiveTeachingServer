"""
Django settings for ActiveTeachingServer project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
from . credentials import SECRET_KEY, DB_NAME, DB_PASSWORD, DB_USER, \
    EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'u9syfm&2lrnemk&5vvi8wib1m^j=!anb@y%a^nnl2(qakn*m&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "activeteaching.research.comnet.aalto.fi"]

# Application definition

INSTALLED_APPS = [
    'experimental_condition.apps.ExperimentalConditionConfig',
    'teaching.apps.TeachingConfig',
    'user.apps.UserConfig',
    'teaching_material.apps.TeachingMaterialConfig',
    'reception_desk.apps.TaskConfig',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ActiveTeachingServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ActiveTeachingServer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '',
        'PORT': '5432',
        # 'ATOMIC_REQUESTS': True,
    },
}

# Keep the default database when testing
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '',
        'PORT': '5432',
        'CONN_MAX_AGE': None
    # 'ATOMIC_REQUESTS': True,
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


# Channels
ASGI_APPLICATION = 'ActiveTeachingServer.routing.application'

AUTH_USER_MODEL = 'user.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# os.makedirs('tmp', exist_ok=True)
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    # 'filters': {
    #     'require_debug_false': {
    #         '()': 'django.utils.log.RequireDebugFalse',
    #     },
    #     'require_debug_true': {
    #         '()': 'django.utils.log.RequireDebugTrue',
    #     },
    # },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django-debug.log',   # os.path.join('tmp', 'django-debug.log'),
            'formatter': 'verbose'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django-error.log',   # os.path.join('tmp', 'django-error.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'file_error'],
            'propagate': True,
            'level': 'INFO'
        },
        # 'django.server': {
        #     'handlers': ['file', 'console', 'file_error'],
        #     'propagate': True,
        #     'level': 'INFO'
        # },
        'django.request': {
            'handlers': ['console', 'file', 'file_error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console', 'file', 'file_error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'daphne': {
            'handlers': ['console', 'file', 'file_error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # 'daphne.server': {
        #     'handlers': ['file', 'file_error'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
    },
}

# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# SECURE_REFERRER_POLICY = 'no-referrer'

# SECURE_HSTS_SECONDS = 60
