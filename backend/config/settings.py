"""
Django settings for config project.
"""

from pathlib import Path


# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = 'django-insecure-n)2cnlw-llrc9!nf)w#rppr8geu*6ikyq$s-0mk^fk!hp(&br+'

DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',


    # Third party
    'rest_framework',


    # Local apps
    'accounts',

    'administrative_classes',

    'counselors',

    'students',

    'attendance',
    'leaves',
    "corsheaders",
]



MIDDLEWARE = [

   "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]



ROOT_URLCONF = 'config.urls'



TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]



WSGI_APPLICATION = 'config.wsgi.application'



# Database

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'student_attendance_db',

        'USER': 'root',

        'PASSWORD': 'Student@2026',

        'HOST': 'localhost',

        'PORT': '3306',

    }

}



# Custom User Model

AUTH_USER_MODEL = 'accounts.CustomUser'



# Password validation

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]



# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files

STATIC_URL = 'static/'



# Media files (QR codes)

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'



# Django REST Framework + JWT

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

}



# Default primary key

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]