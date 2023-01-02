"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

DEBUG = True
SECRET_KEY='django-insecure-wg(wplo(x!$a(l$rzw5k!tr4v#k9zxy5=o_7*9@a(_q4f&3s&8'
ALLOWED_HOSTS=[
    'localhost',
    '127.0.0.1',
    '178.128.94.215',
    'ec2-15-206-185-206.ap-south-1.compute.amazonaws.com',
    'dev.ikhwanbd.com',
    'devadmin.ikhwanbd.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'madrasha_db',
        'USER': 'madrasha',
        'PASSWORD': 'madrasha',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # 3rd party app
    'corsheaders',
    'drf_yasg',  # for swagger
    'django_filters',
    # project app
    'accounts',
    'settingapp',
    'teachers',
    'students',
    'transactions',
    'boarding',
    'library',
    'committees',
    'talimats',
    'transport',
    'darul_ekama',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # for corsheaders
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# ======================Custom User=====================
AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# password hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
# if DEBUG:
#     STATICFILES_DIRS = (os.path.join(BASE_DIR / 'static'),)
# else:
#     STATIC_ROOT = os.path.join(BASE_DIR / 'static')

STATIC_ROOT = os.path.join(BASE_DIR / 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

try:
    from .local_settings import *
except ImportError:
    pass

REST_FRAMEWORK = {
    # for custom pagination in mixin
    # 'DEFAULT_PAGINATION_CLASS': 'students.pagination.CustomPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # <-- And here
    ],

}

# if DEBUG:
#     CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8087',
#                             'http://178.128.94.215:1337',
#                             'http://178.128.94.215',
#                             "http://ec2-15-206-185-206.ap-south-1.compute.amazonaws.com:1337",
#                             "https://dev.ikhwanbd.com",
#                             "http://devadmin.ikhwanbd.com"
#                             ]
# else:
#     CSRF_TRUSTED_ORIGINS = [
#         'http://178.128.94.215:1337',
#         "http://178.128.94.215",
#         "http://ec2-15-206-185-206.ap-south-1.compute.amazonaws.com:1337",
#         "https://dev.ikhwanbd.com",
#         "http://devadmin.ikhwanbd.com"
#     ]


CSRF_TRUSTED_ORIGINS = [
        'http://178.128.94.215:1337',
        "http://178.128.94.215",
        "http://ec2-15-206-185-206.ap-south-1.compute.amazonaws.com:1337",
        "https://dev.ikhwanbd.com",
        "http://devadmin.ikhwanbd.com:1337"
    ]

## SMS Settings

SMS_API_ENDPOINT = "https://api.syssms.syssolution.com.bd/smsapiv3"
SMS_API_KEY = "17002bc09f55fa102ed6586c82ea7b3e"
SMS_SENDER = "8801552146318"
# SMS_ACTIVE = True
SMS_ACTIVE = False
