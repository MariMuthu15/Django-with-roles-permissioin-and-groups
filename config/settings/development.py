from .base import *
import os
from datetime import timedelta

from dotenv import load_dotenv


# env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv()


DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_ALL_ORIGIN = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
    ]

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
    'rest_framework_simplejwt',
    'user',
    'core'
]

DB_NAME = os.getenv('DB_NAME')
DB_ENGINE = os.getenv('DB_ENGINE')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    # 'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',)
}

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

MEDIA_URL = '/media/'

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

