from phaistos.settings.common import *
import os
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ze7xy@oo3m#6g-%gs@)@49jvvrxw^&bgagkqby)sc1!kk95j7^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', '192.168.1.4', '192.168.2.160', '192.168.2.79']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = '/home/gstam/src/phaistos/hope/phaistos/app/static_files/'
# STATICFILES_DIRS = [
#     BASE_DIR / "static_files",
# ]
# print(STATICFILES_DIRS)
# print(f'My base dir is: {os.path.join(BASE_DIR, "..", "static_files")}')
