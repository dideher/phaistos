import os
from phaistos.settings.common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY', 'some-secret-key')

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', 'phaistos.dide.ira.net']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'phaistos_db'),
        'USER': os.environ.get('DB_USER', 'phaistos'),
        'PASSWORD': os.environ.get('DB_PASS', 'phaistos'),
        'HOST': os.environ.get('DB_HOST', 'mysql'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET default_storage_engine=INNODB; SET sql_mode='STRICT_TRANS_TABLES'",
            'isolation_level': 'read committed',
        }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# STATIC_ROOT = '/app/static_files'
MEDIA_ROOT = '/app/media_files'