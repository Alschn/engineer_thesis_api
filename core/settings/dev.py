from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'development')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'postgres_db'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

DEBUG_AUTHENTICATION_CLASSES = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
)

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'accounts.authentication.JWTAuthentication',
        *DEBUG_AUTHENTICATION_CLASSES,
    ),
}

CORS_ORIGIN_WHITELIST = (
    # client app 1
    'http://0.0.0.0:3001',
    'http://localhost:3001',
    'http://127.0.0.1:3001',

    # client app 2
    'http://0.0.0.0:3002',
    'http://localhost:3002',
    'http://127.0.0.1:3002'
)

SHELL_PLUS_IMPORTS = (
    'from core.shared.factories import UserFactory, ProfileFactory, PostFactory, TagFactory, CommentFactory',
)
