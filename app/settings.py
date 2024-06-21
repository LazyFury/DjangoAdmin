"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from better_exceptions.integrations.django import skip_errors_filter


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7@7=#!%y34%t)pd1ch=uh@w++oq4(t&#5_1v58#p@4+7*soucx"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "modules.posts",
    "modules.forms",
    "modules.invite",
    "modules.settings",
    "modules.store",
]

AUTH_USER_MODEL = "core.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.cors_middleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"
ASGI_APPLICATION = "app.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            # "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": DATETIME_FORMAT,
        },
    },
    "filters": {
        "skip_errors": {
            "()": "django.utils.log.CallbackFilter",
            "callback": skip_errors_filter,
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            # without the 'filters' key, Django will log errors twice:
            # one time from better-exceptions and one time from Django.
            # with the 'skip_errors' filter, we remove the repeat log
            # from Django, which is unformatted.
            "filters": ["skip_errors"],
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
        }
    },
}


AUTH_WHITE_LIST = [
    "/admin/api/login",
    "/admin/api/logout",
    # "/admin/api/common/upload",
]
## 权限默认的content_type_id
PERMISSION_DEFAULT_CONTENT_TYPE_ID = 8

LOCKING_DELETE_TABLES = ["settings_dictgroup", "settings_dict"]
LOCKING_MODIFY_TABLES = []

ALLOW_FILE_TYPE = ["image/png", "image/jpeg", "image/gif", "video/mp4"]
ALLOW_IMAGE_TYPE = ["image/png", "image/jpeg", "image/gif"]
ALLOW_VIDEO_TYPE = ["video/mp4","video/avi","video/wmv","video/flv","video/3gp"]
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB
