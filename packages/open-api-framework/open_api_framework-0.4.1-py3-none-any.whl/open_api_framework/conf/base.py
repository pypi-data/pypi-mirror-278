import os
import warnings
from pathlib import Path
from typing import Callable

from django.urls import reverse_lazy

import sentry_sdk
from corsheaders.defaults import default_headers as default_cors_headers
from log_outgoing_requests.formatters import HttpFormatter
from notifications_api_common.settings import *  # noqa

from .utils import (
    config,
    get_django_project_dir,
    get_project_dirname,
    get_sentry_integrations,
    strip_protocol_from_origin,
)

PROJECT_DIRNAME = get_project_dirname()

# Build paths inside the project, so further paths can be defined relative to
# the code root.
DJANGO_PROJECT_DIR = get_django_project_dir()
BASE_DIR = Path(DJANGO_PROJECT_DIR).resolve().parents[1]


#
# Core Django settings
#
SITE_ID = config("SITE_ID", default=1)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# NEVER run with DEBUG=True in production-like environments
DEBUG = config("DEBUG", default=False)

# = domains we're running on
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", split=True)
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", default=False)

IS_HTTPS = config("IS_HTTPS", default=not DEBUG)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "UTC"  # note: this *may* affect the output of DRF datetimes

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

#
# DATABASE and CACHING setup
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", PROJECT_DIRNAME),
        "USER": config("DB_USER", PROJECT_DIRNAME),
        "PASSWORD": config("DB_PASSWORD", PROJECT_DIRNAME),
        "HOST": config("DB_HOST", "localhost"),
        "PORT": config("DB_PORT", 5432),
    }
}

# keep the current schema for now and deal with migrating to BigAutoField later, see
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_DEFAULT', 'localhost:6379/0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "axes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_AXES', 'localhost:6379/0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "oidc": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_DEFAULT', 'localhost:6379/0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

#
# APPLICATIONS enabled for this project
#
INSTALLED_APPS = [
    # Note: contenttypes should be first, see Django ticket #10827
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    # Note: If enabled, at least one Site object is required
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Optional applications.
    "django_admin_index",
    "ordered_model",
    "django.contrib.admin",
    # External applications.
    "axes",
    "django_filters",
    "corsheaders",
    "vng_api_common",
    "notifications_api_common",
    "drf_spectacular",
    "rest_framework",
    "django_markup",
    "solo",
    # Two-factor authentication in the Django admin, enforced.
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "two_factor",
    "two_factor.plugins.webauthn",
    "maykin_2fa",
    "privates",
    "django_jsonform",
    "simple_certmanager",
    "zgw_consumers",
    "mozilla_django_oidc",
    "mozilla_django_oidc_db",
    "log_outgoing_requests",
    "django_setup_configuration",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "maykin_2fa.middleware.OTPMiddleware",
    "mozilla_django_oidc_db.middleware.SessionRefresh",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = f"{PROJECT_DIRNAME}.urls"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(DJANGO_PROJECT_DIR) / "templates"],
        "APP_DIRS": False,  # conflicts with explicity specifying the loaders
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                f"{PROJECT_DIRNAME}.utils.context_processors.settings",
            ],
            "loaders": TEMPLATE_LOADERS,
        },
    }
]

WSGI_APPLICATION = f"{PROJECT_DIRNAME}.wsgi.application"

# Translations
LOCALE_PATHS = (Path(DJANGO_PROJECT_DIR) / "conf" / "locale",)

#
# SERVING of static and media files
#

STATIC_URL = "/static/"

STATIC_ROOT = Path(BASE_DIR) / "static"

# Additional locations of static files
STATICFILES_DIRS = [Path(DJANGO_PROJECT_DIR) / "static"]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = Path(BASE_DIR) / "media"

MEDIA_URL = "/media/"

FILE_UPLOAD_PERMISSIONS = 0o644

FIXTURE_DIRS = (Path(DJANGO_PROJECT_DIR) / "fixtures",)

#
# Sending EMAIL
#
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config(
    "EMAIL_PORT", default=25
)  # disabled on Google Cloud, use 487 instead
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False)
EMAIL_TIMEOUT = 10

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", f"{PROJECT_DIRNAME}@example.com")

#
# LOGGING
#
LOG_STDOUT = config("LOG_STDOUT", default=False)
LOG_LEVEL = config("LOG_LEVEL", default="WARNING")
LOG_QUERIES = config("LOG_QUERIES", default=False)
LOG_REQUESTS = config("LOG_REQUESTS", default=False)
if LOG_QUERIES and not DEBUG:
    warnings.warn(
        "Requested LOG_QUERIES=1 but DEBUG is false, no query logs will be emited.",
        RuntimeWarning,
    )

LOGGING_DIR = Path(BASE_DIR) / "log"

logging_root_handlers = ["console"] if LOG_STDOUT else ["project"]
logging_django_handlers = ["console"] if LOG_STDOUT else ["django"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s"
        },
        "timestamped": {"format": "%(asctime)s %(levelname)s %(name)s  %(message)s"},
        "simple": {"format": "%(levelname)s  %(message)s"},
        "performance": {"format": "%(asctime)s %(process)d | %(thread)d | %(message)s"},
        "db": {"format": "%(asctime)s | %(message)s"},
        "outgoing_requests": {"()": HttpFormatter},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "timestamped",
        },
        "console_db": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "db",
        },
        "django": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "django.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "project": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / f"{PROJECT_DIRNAME}.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "performance": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "performance.log",
            "formatter": "performance",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "requests": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "requests.log",
            "formatter": "timestamped",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "log_outgoing_requests": {
            "level": "DEBUG",
            "formatter": "outgoing_requests",
            "class": "logging.StreamHandler",  # to write to stdout
        },
        "save_outgoing_requests": {
            "level": "DEBUG",
            # enabling saving to database
            "class": "log_outgoing_requests.handlers.DatabaseOutgoingRequestsHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": logging_root_handlers,
            "level": "ERROR",
            "propagate": False,
        },
        PROJECT_DIRNAME: {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "mozilla_django_oidc": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
        },
        f"{PROJECT_DIRNAME}.utils.middleware": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "vng_api_common": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console_db"] if LOG_QUERIES else [],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": logging_django_handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "log_outgoing_requests": {
            "handlers": (
                ["log_outgoing_requests", "save_outgoing_requests"]
                if LOG_REQUESTS
                else []
            ),
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

#
# AUTH settings - user accounts, passwords, backends...
#
AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Allow logging in with both username+password and email+password
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    f"{PROJECT_DIRNAME}.accounts.backends.UserModelEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
]

SESSION_COOKIE_NAME = f"{PROJECT_DIRNAME}_sessionid"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

LOGIN_URL = reverse_lazy("admin:login")
LOGIN_REDIRECT_URL = reverse_lazy("admin:index")
LOGOUT_REDIRECT_URL = reverse_lazy("admin:index")

#
# SECURITY settings
#
SESSION_COOKIE_SECURE = IS_HTTPS
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = IS_HTTPS

X_FRAME_OPTIONS = "DENY"

#
# Silenced checks
#
SILENCED_SYSTEM_CHECKS = [
    "rest_framework.W001",
    "debug_toolbar.W006",
]


#
# Increase number of parameters for GET/POST requests
#
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

#
# Custom settings
#
ENVIRONMENT = config("ENVIRONMENT", "")
ENVIRONMENT_SHOWN_IN_ADMIN = True

# Generating the schema, depending on the component
subpath = config("SUBPATH", None)
if subpath:
    if not subpath.startswith("/"):
        subpath = f"/{subpath}"
    SUBPATH = subpath

if "GIT_SHA" in os.environ:
    GIT_SHA = config("GIT_SHA", "")
# in docker (build) context, there is no .git directory
elif (Path(BASE_DIR) / ".git").exists():
    try:
        import git
    except ImportError:
        GIT_SHA = None
    else:
        repo = git.Repo(search_parent_directories=True)
        GIT_SHA = repo.head.object.hexsha
else:
    GIT_SHA = None

RELEASE = config("RELEASE", GIT_SHA)

NUM_PROXIES = config(  # TODO: this also is relevant for DRF settings if/when we have rate-limited endpoints
    "NUM_PROXIES",
    default=1,
    cast=lambda val: int(val) if val is not None else None,
)

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# DJANGO-AXES (6.0+)
#
AXES_CACHE = "axes"  # refers to CACHES setting
# The number of login attempts allowed before a record is created for the
# failed logins. Default: 3
AXES_FAILURE_LIMIT = 10
# If set, defines a period of inactivity after which old failed login attempts
# will be forgotten. Can be set to a python timedelta object or an integer. If
# an integer, will be interpreted as a number of hours. Default: None
AXES_COOLOFF_TIME = 1
# The number of reverse proxies
AXES_IPWARE_PROXY_COUNT = NUM_PROXIES - 1 if NUM_PROXIES else None
# If set, specifies a template to render when a user is locked out. Template
# receives cooloff_time and failure_limit as context variables. Default: None
AXES_LOCKOUT_TEMPLATE = "account_blocked.html"
AXES_LOCKOUT_PARAMETERS = [["ip_address", "user_agent", "username"]]
AXES_BEHIND_REVERSE_PROXY = IS_HTTPS
# By default, Axes obfuscates values for formfields named "password", but the admin
# interface login formfield name is "auth-password", so we want to obfuscate that
AXES_SENSITIVE_PARAMETERS = ["auth-password"]  # nosec

# The default meta precedence order
IPWARE_META_PRECEDENCE_ORDER = (
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",  # <client>, <proxy1>, <proxy2>
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
)

#
# DJANGO-CORS-MIDDLEWARE
#
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", split=True, default=[])
CORS_ALLOWED_ORIGIN_REGEXES = config(
    "CORS_ALLOWED_ORIGIN_REGEXES", split=True, default=[]
)
# Authorization is included in default_cors_headers
CORS_ALLOW_HEADERS = (
    list(default_cors_headers)
    + [
        "accept-crs",
        "content-crs",
    ]
    + config("CORS_EXTRA_ALLOW_HEADERS", split=True, default=[])
)
CORS_EXPOSE_HEADERS = [
    "content-crs",
]
# Django's SESSION_COOKIE_SAMESITE = "Lax" prevents session cookies from being sent
# cross-domain. There is no need for these cookies to be sent, since the API itself
# uses Bearer Authentication.
# we can't easily derive this from django-cors-headers, see also
# https://pypi.org/project/django-cors-headers/#csrf-integration
#
# So we do a best effort attempt at re-using configuration parameters, with an escape
# hatch to override it.
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    split=True,
    default=[strip_protocol_from_origin(origin) for origin in CORS_ALLOWED_ORIGINS],
)
#
# DJANGO-PRIVATES -- safely serve files after authorization
#
PRIVATE_MEDIA_ROOT = Path(BASE_DIR) / "private-media"
PRIVATE_MEDIA_URL = "/private-media/"


#
# NOTIFICATIONS-API-COMMON
#
NOTIFICATIONS_DISABLED = config("NOTIFICATIONS_DISABLED", default=False)

#
# SENTRY - error monitoring
#


def init_sentry(before_send: Callable | None = None):
    SENTRY_DSN = config("SENTRY_DSN", None)

    if SENTRY_DSN:
        SENTRY_CONFIG = {
            "dsn": SENTRY_DSN,
            "release": RELEASE or "RELEASE not set",
            "environment": ENVIRONMENT,
        }

        # Allow projects to define their own before_send filters
        if before_send:
            SENTRY_CONFIG["before_send"] = before_send

        sentry_sdk.init(
            **SENTRY_CONFIG,
            integrations=get_sentry_integrations(),
            send_default_pii=True,
        )


#
# CELERY
#
CELERY_BROKER_URL = config("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")


#
# DJANGO-ADMIN-INDEX
#
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = False
ADMIN_INDEX_AUTO_CREATE_APP_GROUP = False

#
# Mozilla Django OIDC DB settings
#
OIDC_AUTHENTICATE_CLASS = "mozilla_django_oidc_db.views.OIDCAuthenticationRequestView"
MOZILLA_DJANGO_OIDC_DB_CACHE = "oidc"
MOZILLA_DJANGO_OIDC_DB_CACHE_TIMEOUT = 5 * 60

#
# Elastic APM
#
ELASTIC_APM_SERVER_URL = config("ELASTIC_APM_SERVER_URL", None)
ELASTIC_APM = {
    # FIXME this does change the default service name, because PROJECT_DIRNAME != PROJECT_NAME
    "SERVICE_NAME": config(
        "ELASTIC_APM_SERVICE_NAME", f"{PROJECT_DIRNAME} - {ENVIRONMENT}"
    ),
    "SECRET_TOKEN": config("ELASTIC_APM_SECRET_TOKEN", "default"),
    "SERVER_URL": ELASTIC_APM_SERVER_URL,
    "TRANSACTION_SAMPLE_RATE": config("ELASTIC_APM_TRANSACTION_SAMPLE_RATE", 0.1),
}
if not ELASTIC_APM_SERVER_URL:
    ELASTIC_APM["ENABLED"] = False
    ELASTIC_APM["SERVER_URL"] = "http://localhost:8200"
else:
    MIDDLEWARE = ["elasticapm.contrib.django.middleware.TracingMiddleware"] + MIDDLEWARE
    INSTALLED_APPS = INSTALLED_APPS + [
        "elasticapm.contrib.django",
    ]


#
# MAYKIN-2FA
# Uses django-two-factor-auth under the hood, so relevant upstream package settings
# apply too.
#

# we run the admin site monkeypatch instead.
TWO_FACTOR_PATCH_ADMIN = False
# add entries from AUTHENTICATION_BACKENDS that already enforce their own two-factor
# auth, avoiding having some set up MFA again in the project.
MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = [
    "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
]

if config("DISABLE_2FA", default=False):  # pragma: no cover
    MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = AUTHENTICATION_BACKENDS


#
# LOG OUTGOING REQUESTS
#
LOG_OUTGOING_REQUESTS_EMIT_BODY = True
LOG_OUTGOING_REQUESTS_DB_SAVE = config("LOG_OUTGOING_REQUESTS_DB_SAVE", default=False)
LOG_OUTGOING_REQUESTS_RESET_DB_SAVE_AFTER = None
LOG_OUTGOING_REQUESTS_MAX_AGE = config(
    "LOG_OUTGOING_REQUESTS_MAX_AGE", default=7
)  # number of days
