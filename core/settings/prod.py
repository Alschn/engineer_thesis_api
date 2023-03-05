import dj_database_url

from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [
    os.environ['PRODUCTION_HOST']
]

DATABASE_URL = os.environ['DATABASE_URL']

db_from_env = dj_database_url.config(
    default=DATABASE_URL,
    conn_max_age=500,
    conn_health_checks=True,
    ssl_require=True
)

DATABASES['default'].update({
    **db_from_env,
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "OPTIONS": {
        "connect_timeout": 5,
    }
})

CORS_ORIGIN_WHITELIST = (
    os.environ['CLIENT_APP_REACT'],
    os.environ['CLIENT_APP_SVELTE'],
)

SHELL_PLUS_IMPORTS = (
    'from core.shared.factories import UserFactory, ProfileFactory, PostFactory, TagFactory, CommentFactory',
)

CSRF_TRUSTED_ORIGINS = [
    "https://" + os.environ['PRODUCTION_HOST'],
]

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
