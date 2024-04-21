import os
from pathlib import Path
import pymongo

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-j4ippt+3h39u4ontllpc8a(4h&^god(7aicz#@q^sl_(w)2otp'

DEBUG = True

ALLOWED_HOSTS = ['www.campusmarket.tech', '*']

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

STATIC_ROOT = BASE_DIR / "staticfiles" / "static"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'conversation',
    'core',
    'dashboard',
    'item',
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

ROOT_URLCONF = 'puddle.urls'

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

WSGI_APPLICATION = 'puddle.wsgi.application'

# MongoDB configuration
MONGO_DB_NAME = 'campus_market'
MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017

client = pymongo.MongoClient(
    host=MONGO_DB_HOST,
    port=MONGO_DB_PORT,
    # Uncomment the lines below if you're using authentication
    # username=MONGO_DB_USERNAME,
    # password=MONGO_DB_PASSWORD,
)

mongo_db = client['campus_market']

# Use pymongo as the database engine


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.dummy',  # No engine specified for PyMongo
#         'NAME': 'campus_market',  # Database name
#         'HOST': 'localhost',  # MongoDB host
#         'PORT': 27017,  # MongoDB port
#         # Optional: Uncomment and specify credentials if using authentication
#         # 'USERNAME': 'your_username',
#         # 'PASSWORD': 'your_password',
#     }
# }


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
