"""
Django settings for djangoshop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Change on production. Using development database configuration if True.
IN_DEVELOPMENT = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kuzd7hsqt@@zs9w!nrh5i&e*g2u1&2&74$$f@!nujzx^0_*#_$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django_cassandra_engine',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'app_rdbms',
    'app_cassandra',
    'tags',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # only disabled allowing profilerclient.py job. Don't do it in production.
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangoshop.urls'

WSGI_APPLICATION = 'djangoshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

development_mysql = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'djangoshop_rdbms',
    'USER': 'root',
    'PASSWORD': 'trilobite',
    'HOST': 'localhost',
    'PORT': 3306,
    'OPTIONS': {
        'read_default_file': '/etc/mysql/my.cnf',
        'init_command': 'SET storage_engine=INNODB'
    }
}

production_mysql = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'djangoshop_rdbms',
    'USER': 'djangoshop_admz',
    'PASSWORD': '43Erfr_t=12',
    'HOST': 'localhost',
    'PORT': 3306,
    'OPTIONS': {
        'read_default_file': '/etc/mysql/my.cnf',
        'init_command': 'SET storage_engine=INNODB'
    }
}

if IN_DEVELOPMENT:
    default_mysql = development_mysql

else:
    default_mysql = production_mysql

DATABASES = {
    'default': default_mysql,

    'mysql': default_mysql,

    'cassandra': {      # Using authentication is recommended for production.
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'djangoshop_cassandra',
        'HOST': '10.0.0.2',
        'OPTIONS': {
            'replication': {
                'strategy_class': 'SimpleStrategy',
                'replication_factor': 3
            }
        }
    }
}

DATABASE_ROUTERS = [
    'app_rdbms.models.MySQLRouter',
    'app_cassandra.models.CassandraRouter',
]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Using a static resources directory shared by all the apps

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    # custom settings first in root context and also by app
    "djangoshop.context_processors.global_settings",
)

# Custom Constants
# See context_processor.py
PRODUCTS_IMG_DIR = 'images/products/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates/'),)